from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.database import get_db
from app.deps import get_current_user
from app.models.parcel import Parcel, SurveyPlan
from app.models.user import User
from app.schemas.parcel import (
    ParcelCreate,
    ParcelRead,
    SurveyPlanCreate,
    SurveyPlanRead,
    SurveyPlanReview,
)

router = APIRouter(prefix="/parcels", tags=["parcels"])


# ── Survey plans ──────────────────────────────────────────────────────────────

@router.post("/surveys", response_model=SurveyPlanRead, status_code=201)
def submit_survey_plan(
    payload: SurveyPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_permission(current_user.role, "parcel:submit_survey")
    if db.query(SurveyPlan).filter(
        SurveyPlan.reference_number == payload.reference_number
    ).first():
        raise HTTPException(status_code=400, detail="Reference number already exists")
    plan = SurveyPlan(**payload.model_dump(), submitted_by=current_user.id)
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


@router.get("/surveys", response_model=list[SurveyPlanRead])
def list_survey_plans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_permission(current_user.role, "parcel:read_detail")
    return db.query(SurveyPlan).all()


@router.get("/surveys/{plan_id}", response_model=SurveyPlanRead)
def get_survey_plan(
    plan_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_permission(current_user.role, "parcel:read_detail")
    plan = db.get(SurveyPlan, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Survey plan not found")
    return plan


@router.post("/surveys/{plan_id}/review", response_model=SurveyPlanRead)
def review_survey_plan(
    plan_id: str,
    payload: SurveyPlanReview,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_permission(current_user.role, "parcel:approve")
    if payload.status not in ("approved", "rejected"):
        raise HTTPException(status_code=400, detail="status must be 'approved' or 'rejected'")
    plan = db.get(SurveyPlan, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Survey plan not found")
    if plan.status != "pending":
        raise HTTPException(status_code=400, detail="Survey plan is not pending")
    plan.status = payload.status
    plan.review_notes = payload.review_notes
    plan.reviewed_by = current_user.id
    plan.reviewed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(plan)
    return plan


# ── Parcels ───────────────────────────────────────────────────────────────────

@router.get("/", response_model=list[ParcelRead])
def list_parcels(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_permission(current_user.role, "parcel:read_public")
    return db.query(Parcel).all()


@router.get("/{parcel_id}", response_model=ParcelRead)
def get_parcel(
    parcel_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_permission(current_user.role, "parcel:read_public")
    parcel = db.get(Parcel, parcel_id)
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcel not found")
    return parcel


@router.post("/", response_model=ParcelRead, status_code=201)
def create_parcel(
    payload: ParcelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Cadastral officer activates the official parcel after survey approval."""
    require_permission(current_user.role, "parcel:approve")
    plan = db.get(SurveyPlan, payload.survey_plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Survey plan not found")
    if plan.status != "approved":
        raise HTTPException(
            status_code=400,
            detail="Survey plan must be approved before creating a parcel",
        )
    if plan.parcel:
        raise HTTPException(status_code=400, detail="A parcel already exists for this survey plan")
    if db.query(Parcel).filter(
        Parcel.parcel_identifier == payload.parcel_identifier
    ).first():
        raise HTTPException(status_code=400, detail="Parcel identifier already in use")
    parcel = Parcel(**payload.model_dump(), created_by=current_user.id)
    db.add(parcel)
    db.commit()
    db.refresh(parcel)
    return parcel

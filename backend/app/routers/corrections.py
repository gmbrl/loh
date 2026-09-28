from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.database import get_db
from app.deps import get_current_user
from app.models.correction import CorrectionRequest
from app.models.user import User
from app.schemas.correction import (
    CorrectionRequestCreate,
    CorrectionRequestRead,
    CorrectionReview,
)

router = APIRouter(prefix="/corrections", tags=["corrections"])

# Map correction_level → permission to submit
_LEVEL_PERMISSION = {
    "clerical": "correction:submit_clerical",
    "technical": "correction:submit_technical",
    "substantive": "correction:submit_substantive",
}


@router.get("/", response_model=list[CorrectionRequestRead])
def list_corrections(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_permission(current_user.role, "correction:read")
    return db.query(CorrectionRequest).all()


@router.get("/{cr_id}", response_model=CorrectionRequestRead)
def get_correction(
    cr_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_permission(current_user.role, "correction:read")
    cr = db.get(CorrectionRequest, cr_id)
    if not cr:
        raise HTTPException(status_code=404, detail="Correction request not found")
    return cr


@router.post("/", response_model=CorrectionRequestRead, status_code=201)
def submit_correction(
    payload: CorrectionRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    perm = _LEVEL_PERMISSION.get(payload.correction_level)
    if not perm:
        raise HTTPException(status_code=400, detail="Invalid correction_level")
    require_permission(current_user.role, perm)
    if not payload.parcel_id and not payload.title_id:
        raise HTTPException(status_code=400, detail="Either parcel_id or title_id is required")
    cr = CorrectionRequest(**payload.model_dump(), submitted_by=current_user.id)
    db.add(cr)
    db.commit()
    db.refresh(cr)
    return cr


@router.post("/{cr_id}/review", response_model=CorrectionRequestRead)
def review_correction(
    cr_id: str,
    payload: CorrectionReview,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_permission(current_user.role, "correction:approve")
    cr = db.get(CorrectionRequest, cr_id)
    if not cr:
        raise HTTPException(status_code=404, detail="Correction request not found")
    if cr.status not in ("submitted", "under_review"):
        raise HTTPException(status_code=400, detail="Cannot review in current state")
    cr.status = payload.status
    cr.reviewed_by = current_user.id
    cr.review_notes = payload.review_notes
    cr.reviewed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(cr)
    return cr

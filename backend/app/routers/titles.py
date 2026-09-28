from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.database import get_db
from app.deps import get_current_user
from app.models.parcel import Parcel
from app.models.title import Title, TitleApplication, TitleHistory
from app.models.user import User
from app.schemas.title import (
    TitleApplicationCreate,
    TitleApplicationDecision,
    TitleApplicationRead,
    TitleHistoryRead,
    TitleRead,
)

router = APIRouter(prefix="/titles", tags=["titles"])


# ── Applications ──────────────────────────────────────────────────────────────

@router.post("/applications", response_model=TitleApplicationRead, status_code=201)
def create_application(
    payload: TitleApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_permission(current_user.role, "title:submit")
    parcel = db.get(Parcel, payload.parcel_id)
    if not parcel or parcel.status != "active":
        raise HTTPException(status_code=400, detail="Active parcel not found")
    app = TitleApplication(
        **payload.model_dump(),
        submitted_by=current_user.id,
        status="submitted",
    )
    db.add(app)
    db.commit()
    db.refresh(app)
    return app


@router.get("/applications", response_model=list[TitleApplicationRead])
def list_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_permission(current_user.role, "title:read_full")
    return db.query(TitleApplication).all()


@router.get("/applications/{app_id}", response_model=TitleApplicationRead)
def get_application(
    app_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_permission(current_user.role, "title:read_full")
    app = db.get(TitleApplication, app_id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return app


@router.post("/applications/{app_id}/decide", response_model=TitleApplicationRead)
def decide_application(
    app_id: str,
    payload: TitleApplicationDecision,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_permission(current_user.role, "title:approve")
    app = db.get(TitleApplication, app_id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    if app.status not in ("submitted", "under_review"):
        raise HTTPException(status_code=400, detail="Application cannot be decided in its current state")
    app.status = payload.status
    app.registrar_id = current_user.id
    app.registrar_notes = payload.registrar_notes
    app.decided_at = datetime.now(timezone.utc)

    if payload.status == "approved":
        if not payload.title_number:
            raise HTTPException(status_code=400, detail="title_number is required when approving")
        if db.query(Title).filter(Title.title_number == payload.title_number).first():
            raise HTTPException(status_code=400, detail="Title number already exists")
        title = Title(
            title_number=payload.title_number,
            parcel_id=app.parcel_id,
            owner_name=app.proposed_owner_name,
            owner_id_ref=app.proposed_owner_id_ref,
            application_id=app.id,
            registered_by=current_user.id,
        )
        db.add(title)
        db.flush()
        history = TitleHistory(
            title_id=title.id,
            event="registered",
            detail=f"First registration by registrar {current_user.email}",
            recorded_by=current_user.id,
        )
        db.add(history)

    db.commit()
    db.refresh(app)
    return app


# ── Titles ────────────────────────────────────────────────────────────────────

@router.get("/", response_model=list[TitleRead])
def list_titles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_permission(current_user.role, "title:read_public")
    return db.query(Title).all()


@router.get("/{title_id}", response_model=TitleRead)
def get_title(
    title_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_permission(current_user.role, "title:read_public")
    title = db.get(Title, title_id)
    if not title:
        raise HTTPException(status_code=404, detail="Title not found")
    return title


@router.get("/{title_id}/history", response_model=list[TitleHistoryRead])
def get_title_history(
    title_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_permission(current_user.role, "title:read_full")
    title = db.get(Title, title_id)
    if not title:
        raise HTTPException(status_code=404, detail="Title not found")
    return title.history

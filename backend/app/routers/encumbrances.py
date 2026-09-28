from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.permissions import Role, require_permission
from app.database import get_db
from app.deps import get_current_user
from app.models.encumbrance import Encumbrance
from app.models.user import User
from app.schemas.encumbrance import EncumbranceCreate, EncumbranceRead, EncumbranceRelease

router = APIRouter(prefix="/encumbrances", tags=["encumbrances"])

# Map encumbrance_type → permission required to submit it
_SUBMIT_PERMISSION: dict[str, str] = {
    "mortgage": "encumbrance:submit_mortgage",
    "tax_lien": "encumbrance:submit_tax_lien",
    "court_seizure": "encumbrance:submit_court_order",
    "judgment_lien": "encumbrance:submit_court_order",
    "municipal_restriction": "encumbrance:submit_municipal",
    "public_right_of_way": "encumbrance:submit_municipal",
    "lease": "encumbrance:submit_private",
    "easement": "encumbrance:submit_private",
    "adverse_claim": "encumbrance:submit_private",
    "other": "encumbrance:submit_private",
}


@router.get("/", response_model=list[EncumbranceRead])
def list_encumbrances(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_permission(current_user.role, "encumbrance:read_public")
    return db.query(Encumbrance).all()


@router.get("/{enc_id}", response_model=EncumbranceRead)
def get_encumbrance(
    enc_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_permission(current_user.role, "encumbrance:read_public")
    enc = db.get(Encumbrance, enc_id)
    if not enc:
        raise HTTPException(status_code=404, detail="Encumbrance not found")
    return enc


@router.post("/", response_model=EncumbranceRead, status_code=201)
def submit_encumbrance(
    payload: EncumbranceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    perm = _SUBMIT_PERMISSION.get(payload.encumbrance_type)
    if not perm:
        raise HTTPException(status_code=400, detail="Unknown encumbrance type")
    require_permission(current_user.role, perm)
    if not payload.title_id and not payload.parcel_id:
        raise HTTPException(status_code=400, detail="Either title_id or parcel_id is required")
    enc = Encumbrance(**payload.model_dump(), submitted_by=current_user.id)
    db.add(enc)
    db.commit()
    db.refresh(enc)
    return enc


@router.post("/{enc_id}/approve", response_model=EncumbranceRead)
def approve_encumbrance(
    enc_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_permission(current_user.role, "encumbrance:approve")
    enc = db.get(Encumbrance, enc_id)
    if not enc:
        raise HTTPException(status_code=404, detail="Encumbrance not found")
    if enc.status != "pending":
        raise HTTPException(status_code=400, detail="Encumbrance is not pending")
    enc.status = "active"
    enc.approved_by = current_user.id
    enc.approved_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(enc)
    return enc


@router.post("/{enc_id}/release", response_model=EncumbranceRead)
def release_encumbrance(
    enc_id: str,
    payload: EncumbranceRelease,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_permission(current_user.role, "encumbrance:release")
    enc = db.get(Encumbrance, enc_id)
    if not enc:
        raise HTTPException(status_code=404, detail="Encumbrance not found")
    if enc.status != "active":
        raise HTTPException(status_code=400, detail="Encumbrance is not active")
    enc.status = "released"
    enc.released_by = current_user.id
    enc.released_at = datetime.now(timezone.utc)
    enc.release_reference = payload.release_reference
    db.commit()
    db.refresh(enc)
    return enc

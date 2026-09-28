"""
Public query endpoints — tiered access as specified in the authority model.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.database import get_db
from app.deps import get_current_user
from app.models.encumbrance import Encumbrance
from app.models.parcel import Parcel
from app.models.title import Title
from app.models.user import User
from app.schemas.parcel import ParcelRead
from app.schemas.title import TitleRead
from app.schemas.encumbrance import EncumbranceRead

router = APIRouter(prefix="/query", tags=["query"])


@router.get("/parcels", response_model=list[ParcelRead], summary="Search parcels (public)")
def search_parcels(
    identifier: str | None = Query(default=None),
    land_use: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_permission(current_user.role, "parcel:read_public")
    q = db.query(Parcel)
    if identifier:
        q = q.filter(Parcel.parcel_identifier.ilike(f"%{identifier}%"))
    if land_use:
        q = q.filter(Parcel.land_use.ilike(f"%{land_use}%"))
    return q.all()


@router.get("/titles", response_model=list[TitleRead], summary="Search titles (public)")
def search_titles(
    title_number: str | None = Query(default=None),
    parcel_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_permission(current_user.role, "title:read_public")
    q = db.query(Title)
    if title_number:
        q = q.filter(Title.title_number.ilike(f"%{title_number}%"))
    if parcel_id:
        q = q.filter(Title.parcel_id == parcel_id)
    return q.all()


@router.get("/encumbrances", response_model=list[EncumbranceRead], summary="Search encumbrances (public)")
def search_encumbrances(
    title_id: str | None = Query(default=None),
    parcel_id: str | None = Query(default=None),
    enc_type: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_permission(current_user.role, "encumbrance:read_public")
    q = db.query(Encumbrance)
    if title_id:
        q = q.filter(Encumbrance.title_id == title_id)
    if parcel_id:
        q = q.filter(Encumbrance.parcel_id == parcel_id)
    if enc_type:
        q = q.filter(Encumbrance.encumbrance_type == enc_type)
    return q.all()

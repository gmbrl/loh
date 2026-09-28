import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def _now():
    return datetime.now(timezone.utc)


ENCUMBRANCE_TYPES = [
    "mortgage",
    "tax_lien",
    "court_seizure",
    "judgment_lien",
    "municipal_restriction",
    "public_right_of_way",
    "lease",
    "easement",
    "adverse_claim",
    "other",
]


class Encumbrance(Base):
    """A registered interest, restriction, or claim against a title or parcel."""

    __tablename__ = "encumbrances"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    title_id: Mapped[str] = mapped_column(ForeignKey("titles.id"), nullable=True)
    parcel_id: Mapped[str] = mapped_column(ForeignKey("parcels.id"), nullable=True)
    encumbrance_type: Mapped[str] = mapped_column(
        Enum(*ENCUMBRANCE_TYPES, name="encumbrance_type"), nullable=False
    )
    description: Mapped[str] = mapped_column(Text, nullable=True)
    originating_authority: Mapped[str] = mapped_column(String(255), nullable=True)
    instrument_reference: Mapped[str] = mapped_column(String(200), nullable=True)
    # Status: pending | active | released | cancelled
    status: Mapped[str] = mapped_column(
        Enum("pending", "active", "released", "cancelled", name="encumbrance_status"),
        default="pending",
        nullable=False,
    )
    submitted_by: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    approved_by: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=True)
    released_by: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=True)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    approved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    released_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    release_reference: Mapped[str] = mapped_column(Text, nullable=True)

    title = relationship("Title", back_populates="encumbrances")
    parcel = relationship("Parcel", back_populates="encumbrances")
    submitted_by_user = relationship("User", foreign_keys=[submitted_by], back_populates="encumbrance_submissions")
    approved_by_user = relationship("User", foreign_keys=[approved_by])
    released_by_user = relationship("User", foreign_keys=[released_by])

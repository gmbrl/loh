import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def _now():
    return datetime.now(timezone.utc)


class TitleApplication(Base):
    """Pending application for title registration or transfer."""

    __tablename__ = "title_applications"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    parcel_id: Mapped[str] = mapped_column(ForeignKey("parcels.id"), nullable=False)
    instrument_type: Mapped[str] = mapped_column(
        Enum(
            "first_registration",
            "transfer",
            "inheritance",
            "court_order",
            "other",
            name="instrument_type",
        ),
        nullable=False,
    )
    instrument_description: Mapped[str] = mapped_column(Text, nullable=True)
    # Proposed owner name (until registrar approves)
    proposed_owner_name: Mapped[str] = mapped_column(String(255), nullable=False)
    proposed_owner_id_ref: Mapped[str] = mapped_column(String(100), nullable=True)
    # Professional who prepared the instrument
    prepared_by: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=True)
    submitted_by: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    # Status: draft | submitted | under_review | approved | rejected
    status: Mapped[str] = mapped_column(
        Enum(
            "draft",
            "submitted",
            "under_review",
            "approved",
            "rejected",
            name="application_status",
        ),
        default="draft",
        nullable=False,
    )
    registrar_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=True)
    registrar_notes: Mapped[str] = mapped_column(Text, nullable=True)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    submitted_by_user = relationship("User", foreign_keys=[submitted_by], back_populates="title_applications")
    prepared_by_user = relationship("User", foreign_keys=[prepared_by])
    registrar = relationship("User", foreign_keys=[registrar_id])
    parcel = relationship("Parcel")
    title = relationship("Title", back_populates="application", uselist=False)


class Title(Base):
    """Registered title — the authoritative ownership record for a parcel."""

    __tablename__ = "titles"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    title_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    parcel_id: Mapped[str] = mapped_column(ForeignKey("parcels.id"), nullable=False)
    owner_name: Mapped[str] = mapped_column(String(255), nullable=False)
    owner_id_ref: Mapped[str] = mapped_column(String(100), nullable=True)
    # Status: active | transferred | cancelled
    status: Mapped[str] = mapped_column(
        Enum("active", "transferred", "cancelled", name="title_status"),
        default="active",
        nullable=False,
    )
    application_id: Mapped[str] = mapped_column(
        ForeignKey("title_applications.id"), nullable=False
    )
    registered_by: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    parcel = relationship("Parcel", back_populates="titles")
    application = relationship("TitleApplication", back_populates="title")
    registered_by_user = relationship("User", foreign_keys=[registered_by])
    history = relationship(
        "TitleHistory", back_populates="title", order_by="TitleHistory.recorded_at"
    )
    encumbrances = relationship("Encumbrance", back_populates="title")


class TitleHistory(Base):
    """Immutable audit record written whenever a title changes."""

    __tablename__ = "title_history"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    title_id: Mapped[str] = mapped_column(ForeignKey("titles.id"), nullable=False)
    event: Mapped[str] = mapped_column(String(100), nullable=False)
    detail: Mapped[str] = mapped_column(Text, nullable=True)
    recorded_by: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    title = relationship("Title", back_populates="history")
    recorded_by_user = relationship("User", foreign_keys=[recorded_by])

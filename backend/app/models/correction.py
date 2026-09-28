import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def _now():
    return datetime.now(timezone.utc)


class CorrectionRequest(Base):
    """Request to correct a parcel or title record.

    Three levels (per document):
      - clerical: spelling, typo, date, format
      - technical: coordinates, area, boundary description
      - substantive: ownership, priority, fraud, boundary dispute
    """

    __tablename__ = "correction_requests"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    parcel_id: Mapped[str] = mapped_column(ForeignKey("parcels.id"), nullable=True)
    title_id: Mapped[str] = mapped_column(ForeignKey("titles.id"), nullable=True)
    correction_level: Mapped[str] = mapped_column(
        Enum("clerical", "technical", "substantive", name="correction_level"),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_reference: Mapped[str] = mapped_column(Text, nullable=True)
    # Status: submitted | under_review | approved | rejected
    status: Mapped[str] = mapped_column(
        Enum(
            "submitted",
            "under_review",
            "approved",
            "rejected",
            name="correction_status",
        ),
        default="submitted",
        nullable=False,
    )
    submitted_by: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    reviewed_by: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=True)
    review_notes: Mapped[str] = mapped_column(Text, nullable=True)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    reviewed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    submitted_by_user = relationship("User", foreign_keys=[submitted_by], back_populates="correction_requests")
    reviewed_by_user = relationship("User", foreign_keys=[reviewed_by])
    parcel = relationship("Parcel", back_populates="correction_requests")
    title = relationship("Title")

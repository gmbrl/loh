from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TitleApplicationCreate(BaseModel):
    parcel_id: str
    instrument_type: str
    instrument_description: Optional[str] = None
    proposed_owner_name: str
    proposed_owner_id_ref: Optional[str] = None


class TitleApplicationRead(BaseModel):
    id: str
    parcel_id: str
    instrument_type: str
    instrument_description: Optional[str]
    proposed_owner_name: str
    proposed_owner_id_ref: Optional[str]
    prepared_by: Optional[str]
    submitted_by: str
    status: str
    registrar_id: Optional[str]
    registrar_notes: Optional[str]
    submitted_at: datetime
    decided_at: Optional[datetime]

    model_config = {"from_attributes": True}


class TitleApplicationDecision(BaseModel):
    status: str  # "approved" | "rejected" | "under_review"
    registrar_notes: Optional[str] = None
    # Required when approving: title number to assign
    title_number: Optional[str] = None


class TitleRead(BaseModel):
    id: str
    title_number: str
    parcel_id: str
    owner_name: str
    owner_id_ref: Optional[str]
    status: str
    application_id: str
    registered_by: str
    registered_at: datetime

    model_config = {"from_attributes": True}


class TitleHistoryRead(BaseModel):
    id: str
    title_id: str
    event: str
    detail: Optional[str]
    recorded_by: str
    recorded_at: datetime

    model_config = {"from_attributes": True}

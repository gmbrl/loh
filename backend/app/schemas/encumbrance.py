from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EncumbranceCreate(BaseModel):
    title_id: Optional[str] = None
    parcel_id: Optional[str] = None
    encumbrance_type: str
    description: Optional[str] = None
    originating_authority: Optional[str] = None
    instrument_reference: Optional[str] = None


class EncumbranceRead(BaseModel):
    id: str
    title_id: Optional[str]
    parcel_id: Optional[str]
    encumbrance_type: str
    description: Optional[str]
    originating_authority: Optional[str]
    instrument_reference: Optional[str]
    status: str
    submitted_by: str
    approved_by: Optional[str]
    released_by: Optional[str]
    submitted_at: datetime
    approved_at: Optional[datetime]
    released_at: Optional[datetime]
    release_reference: Optional[str]

    model_config = {"from_attributes": True}


class EncumbranceRelease(BaseModel):
    release_reference: str

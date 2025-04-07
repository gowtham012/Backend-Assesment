from pydantic import BaseModel, EmailStr
from datetime import datetime
import enum

class LeadState(str, enum.Enum):
    PENDING = "PENDING"
    REACHED_OUT = "REACHED_OUT"

class LeadBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    resume: str

class LeadCreate(LeadBase):
    pass

class LeadUpdate(BaseModel):
    state: LeadState

class LeadOut(LeadBase):
    id: int
    state: LeadState
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

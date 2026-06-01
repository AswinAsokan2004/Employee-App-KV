from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    name: str


class DepartmentUpdate(BaseModel):
    name: str


class DepartmentPatch(BaseModel):
    name: Optional[str] = None


class DepartmentResponse(BaseModel):
    id: int
    name: str

    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

class MessageResponds(BaseModel):
    message: str
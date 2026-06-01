from typing import Optional

from pydantic import BaseModel, ConfigDict


class AddressCreate(BaseModel):
    line1: str
    city: str
    postal_code: str
    country: str


class AddressUpdate(BaseModel):
    line1: str
    city: str
    postal_code: str
    country: str


class AddressPatch(BaseModel):
    line1: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None


class AddressResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    # id: int
    # employee_id: int

    line1: str
    city: str
    postal_code: str
    country: str

    # created_at: datetime | None = None
    # updated_at: datetime | None = None
    # deleted_at: datetime | None = None
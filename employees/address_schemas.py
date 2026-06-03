from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from exceptions.exceptions import ConflictException


class AddressCreate(BaseModel):
    line1: str
    city: str
    postal_code: str
    country: str

    @field_validator("postal_code")
    @classmethod
    def validate_postalcode(cls, v: str) -> str:
        """Validate"""
        if not v.isdigit():
            raise ConflictException("Postal code should only be a number")
        return v

    @model_validator(mode="after")
    def postal_code_length_for_country(self):
        country = self.country.strip().upper()
        n = len(self.postal_code)
        if country in ("US", "USA") and n != 5:
            raise ConflictException("US ZIP codes must be exactly 5 digits")
        elif country == "IN" and n != 6:
            raise ConflictException("Indian PIN codes must be exactly 6 digits")
        return self


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
    model_config = ConfigDict(from_attributes=True)
    id: int
    employee_id: int

    line1: str
    city: str
    postal_code: str
    country: str

    # created_at: datetime | None = None
    # updated_at: datetime | None = None
    # deleted_at: datetime | None = None

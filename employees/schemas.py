from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    EmailStr,
    model_validator,
)


class AddressCreate(BaseModel):
    line1: str
    city: str
    country: str
    postalcode: str

    @field_validator("postalcode")
    @classmethod
    def validate_postalcode(cls, v: str) -> str:
        """Validate"""
        if not v.isdigit():
            raise ValueError("Postal code should only be a number")
        return v

    @model_validator(mode="after")
    def postal_code_length_for_country(self):
        country = self.country.strip().upper()
        n = len(self.postalcode)
        if country in ("US", "USA") and n != 5:
            raise ValueError("US ZIP codes must be exactly 5 digits")
        elif country == "IN" and n != 6:
            raise ValueError("Indian PIN codes must be exactly 6 digits")
        return self


class EmployeeCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    name: str
    email: EmailStr
    age: int | None = Field(ge=0, le=150, default=None)
    password: str
    address: AddressCreate | None = None


class EmployeeResponds(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    age: int | None


class EmployeeGetByIDResponds(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    age: int | None


class loginRequest(BaseModel):
    email: EmailStr
    password: str


class loginResponds(BaseModel):
    token: str


class EmployeeUpdate(BaseModel):
    name: str
    email: EmailStr
    age: int


class EmployeePatch(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None


class MessageResponds(BaseModel):
    message: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str

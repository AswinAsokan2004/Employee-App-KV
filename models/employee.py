"""
Employee entity — ORM mapped class for table `employees`.
"""

from datetime import datetime
import enum
from typing import Any, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.entity import Entity
from models.employee_department import employee_departments
from models.department import Department
from sqlalchemy import Enum

def _datetime_to_iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat()


class EmployeeRole(str, enum.Enum):
    UI = "UI"
    UX = "UX"
    DEVELOPER = "DEVELOPER"
    HR = "HR"
    
class Address(Entity):
    __abstract__ = False
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    employee_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    line1: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)

    # employees: Mapped["Employee"] = relationship("Employee", back_populates="addresses")
    employee: Mapped["Employee"] = relationship(
            "Employee",
            back_populates="addresses"
    )
    def to_api_dict(self) -> dict[str, Any]:
        """JSON-friendly representation (ISO 8601 for timestamps)."""
        return {
            "id": self.id,
            "line1": self.line1,
            "city": self.city,
            "postal_code": self.postal_code,
            "country": self.country,
            "created_at": _datetime_to_iso(self.created_at),
            "updated_at": _datetime_to_iso(self.updated_at),
            "deleted_at": _datetime_to_iso(self.deleted_at)
        }

class Employee(Entity):
    __abstract__ = False
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    role: Mapped[EmployeeRole] = mapped_column(
        Enum(EmployeeRole, name = "employeerole"),
        nullable=False,
        server_default=EmployeeRole.DEVELOPER.value
    )
    # address: Mapped["Address"] = relationship("Address", back_populates="Employee")
    addresses: Mapped[list["Address"]] = relationship(
        "Address",
        back_populates="employee",
        cascade="all, delete-orphan"
    )
    departments: Mapped[list["Department"]] = relationship(
        "Department",
        secondary=employee_departments,
        back_populates="employees"
    )

    def to_api_dict(self) -> dict[str, Any]:
        """JSON-friendly representation (ISO 8601 for timestamps)."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "created_at": _datetime_to_iso(self.created_at),
            "updated_at": _datetime_to_iso(self.updated_at),
            "deleted_at": _datetime_to_iso(self.deleted_at)
        }
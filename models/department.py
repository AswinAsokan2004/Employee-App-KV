from typing import TYPE_CHECKING, Any

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from models.entity import Entity, datetime_to_iso
from sqlalchemy.orm import relationship
from models.employee_department import employee_departments

if TYPE_CHECKING:
    from models.department import Department

if TYPE_CHECKING:
    from models.employee import Employee


class Department(Entity):
    __abstract__ = False
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    employees: Mapped[list["Employee"]] = relationship(
        "Employee", secondary=employee_departments, back_populates="departments"
    )

    def to_api_dict(self) -> dict[str, Any]:
        """JSON-friendly representation (ISO 8601 for timestamps)."""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": datetime_to_iso(self.created_at),
            "updated_at": datetime_to_iso(self.updated_at),
            "deleted_at": datetime_to_iso(self.deleted_at),
        }

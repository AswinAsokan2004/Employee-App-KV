from sqlalchemy import Table, Column, ForeignKey, Integer

from database.connection import Base

employee_departments = Table(
    "employee_departments",
    Base.metadata,

    Column(
        "employee_id",
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        primary_key=True
    ),

    Column(
        "department_id",
        Integer,
        ForeignKey("departments.id", ondelete="CASCADE"),
        primary_key=True
    )
)
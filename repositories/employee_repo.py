from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.employee import Employee
from sqlalchemy.exc import IntegrityError
from fastapi import status


async def create(name: str, email: str, db: AsyncSession) -> Employee:
    db_employee = Employee(name=name.strip(), email=email.strip())
    db.add(db_employee)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{email.strip()}' is already in use",
        ) from exc
    await db.refresh(db_employee)
    return db_employee


async def get_all_employee(db: AsyncSession):
    stmt = select(Employee).where(Employee.deleted_at.is_(None))
    result = await db.scalars(stmt)
    return result


async def get_employee_by_id(db: AsyncSession, employee_id: int) -> Employee:
    stmt = select(Employee).where(
        Employee.deleted_at.is_(None), Employee.id == employee_id
    )
    result = await db.scalar(stmt)
    return result

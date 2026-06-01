from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.department import Department


async def create(
    name: str,
    db: AsyncSession
):
    department = Department(
        name=name.strip()
    )

    db.add(department)

    try:
        await db.commit()

    except IntegrityError as exc:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Department already exists"
        ) from exc

    await db.refresh(department)

    return department


async def get_all(
    db: AsyncSession
):
    stmt = select(Department).where(
        Department.deleted_at.is_(None)
    )

    result = await db.scalars(stmt)

    return result.all()


async def get_by_id(
    department_id: int,
    db: AsyncSession
):
    stmt = select(Department).where(
        Department.id == department_id,
        Department.deleted_at.is_(None)
    )

    result = await db.scalar(stmt)

    return result


async def update(
    department_id: int,
    name: str,
    db: AsyncSession
):
    department = await get_by_id(
        department_id=department_id,
        db=db
    )

    if department is None:
        return None

    department.name = name.strip()

    await db.commit()

    await db.refresh(department)

    return department


async def patch(
    department_id: int,
    data: dict,
    db: AsyncSession
):
    department = await get_by_id(
        department_id=department_id,
        db=db
    )

    if department is None:
        return None

    for key, value in data.items():
        setattr(department, key, value)

    await db.commit()

    await db.refresh(department)

    return department


async def delete(
    department_id: int,
    db: AsyncSession
):
    department = await get_by_id(
        department_id=department_id,
        db=db
    )

    if department is None:
        return None

    department.deleted_at = datetime.utcnow()

    await db.commit()

    return department
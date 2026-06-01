from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.employee import Address


async def create(
    employee_id: int,
    line1: str,
    city: str,
    postal_code: str,
    country: str,
    db: AsyncSession,
):
    address = Address(
        employee_id=employee_id,
        line1=line1,
        city=city,
        postal_code=postal_code,
        country=country,
    )

    db.add(address)

    await db.commit()

    await db.refresh(address)

    return address


async def get_all(db: AsyncSession):
    stmt = select(Address).where(Address.deleted_at.is_(None))

    result = await db.scalars(stmt)

    return result.all()


async def get_by_id(address_id: int, db: AsyncSession):
    stmt = select(Address).where(Address.id == address_id, Address.deleted_at.is_(None))

    result = await db.scalar(stmt)

    return result


async def get_by_employee_id(employee_id: int, db: AsyncSession):
    stmt = select(Address).where(
        Address.employee_id == employee_id, Address.deleted_at.is_(None)
    )

    result = await db.scalars(stmt)

    return result.all()


async def update(
    address_id: int,
    line1: str,
    city: str,
    postal_code: str,
    country: str,
    db: AsyncSession,
):
    address = await get_by_id(address_id=address_id, db=db)

    if address is None:
        return None

    address.line1 = line1
    address.city = city
    address.postal_code = postal_code
    address.country = country

    await db.commit()

    await db.refresh(address)

    return address


async def patch(address_id: int, data: dict, db: AsyncSession):
    address = await get_by_id(address_id=address_id, db=db)

    if address is None:
        return None

    for key, value in data.items():
        setattr(address, key, value)

    await db.commit()

    await db.refresh(address)

    return address


async def delete(address_id: int, db: AsyncSession):
    address = await get_by_id(address_id=address_id, db=db)

    if address is None:
        return None

    address.deleted_at = datetime.utcnow()

    await db.commit()

    return address

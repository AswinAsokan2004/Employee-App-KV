from sqlalchemy.ext.asyncio import AsyncSession

from employees import address_repo
from exceptions.exceptions import NotFoundException


async def create(
    employee_id: int,
    line1: str,
    city: str,
    postal_code: str,
    country: str,
    db: AsyncSession,
):
    result = await address_repo.create(
        employee_id=employee_id,
        line1=line1,
        city=city,
        postal_code=postal_code,
        country=country,
        db=db,
    )

    return result.to_api_dict()


async def get_all(db: AsyncSession):
    result = await address_repo.get_all(db=db)

    return [address.to_api_dict() for address in result]


async def get_by_id(address_id: int, db: AsyncSession):
    result = await address_repo.get_by_id(address_id=address_id, db=db)

    if result is None:
        raise NotFoundException(detail="Address not found")

    return result.to_api_dict()


async def get_by_employee_id(employee_id: int, db: AsyncSession):
    result = await address_repo.get_by_employee_id(employee_id=employee_id, db=db)

    return [address.to_api_dict() for address in result]


async def update(
    address_id: int,
    line1: str,
    city: str,
    postal_code: str,
    country: str,
    db: AsyncSession,
):
    result = await address_repo.update(
        address_id=address_id,
        line1=line1,
        city=city,
        postal_code=postal_code,
        country=country,
        db=db,
    )

    if result is None:
        raise NotFoundException(detail="Address not found")

    return result.to_api_dict()


async def patch(address_id: int, data: dict, db: AsyncSession):
    result = await address_repo.patch(address_id=address_id, data=data, db=db)

    if result is None:
        raise NotFoundException(detail="Address not found")

    return result.to_api_dict()


async def delete(address_id: int, db: AsyncSession):
    result = await address_repo.delete(address_id=address_id, db=db)

    if result is None:
        raise NotFoundException(detail="Address not found")

    return {"message": "Address deleted successfully"}

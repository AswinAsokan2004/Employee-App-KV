from sqlalchemy.ext.asyncio import AsyncSession

from departments import department_repo
from exceptions.exceptions import NotFoundException


async def create(name: str, db: AsyncSession):
    result = await department_repo.create(name=name, db=db)

    return result.to_api_dict()


async def get_all(db: AsyncSession):
    result = await department_repo.get_all(db=db)

    return [department.to_api_dict() for department in result]


async def get_by_id(department_id: int, db: AsyncSession):
    result = await department_repo.get_by_id(department_id=department_id, db=db)

    if result is None:
        raise NotFoundException(detail="Department not found")

    return result.to_api_dict()


async def update(department_id: int, name: str, db: AsyncSession):
    result = await department_repo.update(department_id=department_id, name=name, db=db)

    if result is None:
        raise NotFoundException(detail="Department not found")

    return result.to_api_dict()


async def patch(department_id: int, data: dict, db: AsyncSession):
    result = await department_repo.patch(department_id=department_id, data=data, db=db)

    if result is None:
        raise NotFoundException(detail="Department not found")

    return result.to_api_dict()


async def delete(department_id: int, db: AsyncSession):
    result = await department_repo.delete(department_id=department_id, db=db)

    if result is None:
        raise NotFoundException(detail="Department not found")

    return {"message": f"Department {department_id} deleted successfully"}

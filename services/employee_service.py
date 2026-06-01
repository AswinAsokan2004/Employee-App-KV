from fastapi import HTTPException
from fastapi import status
from employees import employee_repo
from sqlalchemy.ext.asyncio import AsyncSession


async def create(name: str, email: str, db: AsyncSession):
    if not isinstance(name, str) or not name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="name must be a non-empty string",
        )
    if not isinstance(email, str) or not email.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email must be a non-empty string",
        )
    employee = await employee_repo.create(name=name, email=email, db=db)
    return employee


async def get_all_employee(db: AsyncSession):
    result = await employee_repo.get_all_employee(db=db)
    return [r.to_api_dict() for r in result.all()]


async def get_employee_by_id(employee_id: int, db: AsyncSession):
    result = await employee_repo.get_employee_by_id(employee_id=employee_id, db=db)
    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")
    return result.to_api_dict()

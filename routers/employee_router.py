from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from services import employee_service

router = APIRouter(prefix='/employee')

@router.post("/create", status_code=status.HTTP_201_CREATED, tags=["Employees"])
async def create(db: AsyncSession = Depends(get_db), body: dict = Body(...)):
    name = body.get("name")
    email = body.get("email")
    result = await employee_service.create(name=name, email=email, db=db)
    return result.to_api_dict()

@router.get("/get", status_code=status.HTTP_200_OK, tags=["Employees"])
async def get_all_employees(db: AsyncSession = Depends(get_db)):
    result = await employee_service.get_all_employee(db=db)
    return result

@router.get("/get/{id}", status_code=status.HTTP_200_OK, tags=["Employees"])
async def get_all_employees_by_id(id: int, db: AsyncSession = Depends(get_db)):
    print(f"employee id = {id}")
    result = await employee_service.get_employee_by_id(db=db, employee_id=id)
    return result
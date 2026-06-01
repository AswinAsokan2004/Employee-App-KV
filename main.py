import logging
from sqlite3 import IntegrityError

from fastapi import Body, Depends, FastAPI, HTTPException, Request, status
from typing import List, TypedDict
from dataclasses import dataclass

from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse
from sqlalchemy import delete, select
from config import Settings
from exceptions.exceptions import AppException, NotFoundException, ConflictException, BadRequestException
from middleware import configure_middleware
from middleware.logger import RequestLoggingMiddleware
from fastapi.middleware.cors import CORSMiddleware
from database.connection import create_tables, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from models.employee import Employee

from repositories.employee_repo import create
from routers import employee_router
from routers.employee_router import router as employee_router_pack
import pdb

from employees.router import router as package_router
from departments.department_router import router_dep
from employees.address_router import router_address
from exceptions.handler import register_exception_handler
from config import settings
from auth.router import router_auth

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await create_tables()
#    

    
app = FastAPI(
    title="Employee CRUD Application", 
    description="A simple CRUD application for managing employees.",
    version="1.0.0",
    # lifespan=lifespan
)
register_exception_handler(app=app)
configure_middleware(app)

app.include_router(package_router)
app.include_router(router_dep)
app.include_router(router_address)
app.include_router(router_auth)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "env": settings.app_env}


@app.post("/employee/create", status_code=status.HTTP_201_CREATED, tags=["Employees"])
async def create_employee(body: dict = Body(...)):
    
    result = await employee_router.create(body=body)
    return result

from sqlalchemy import select, update
from fastapi import HTTPException

@app.patch("/employee/patch/{id}", tags=["Employees"])
async def update_employee_by_id(
    id: int,
    name: str | None = None,
    email: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Employee).where(
        Employee.deleted_at.is_(None),
        Employee.id == id
    )

    employee = await db.scalar(stmt)

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    update_data = {}

    if name is not None:
        update_data["name"] = name

    if email is not None:
        update_data["email"] = email

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    stmt = (
        update(Employee)
        .where(Employee.id == id)
        .values(**update_data)
    )

    await db.execute(stmt)
    await db.commit()

    updated_employee = await db.scalar(
        select(Employee).where(Employee.id == id)
    )

    return updated_employee.to_api_dict()


@app.put("/employee/patch/{id}", tags=["Employees"])
async def update_employee_full_by_id(
    id: int,
    name: str,
    email: str,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Employee).where(
        Employee.deleted_at.is_(None),
        Employee.id == id
    )

    employee = await db.scalar(stmt)

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    update_data = {}

    if name is not None:
        update_data["name"] = name

    if email is not None:
        update_data["email"] = email

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    stmt = (
        update(Employee)
        .where(Employee.id == id)
        .values(**update_data)
    )

    await db.execute(stmt)
    await db.commit()

    updated_employee = await db.scalar(
        select(Employee).where(Employee.id == id)
    )

    return updated_employee.to_api_dict()


@app.delete("/employee/delete/{id}", tags=['Employees'])
async def employee_delete_by_id(id: int, db: AsyncSession = Depends(get_db)):
    stmt = delete(Employee).where(Employee.id == id)
    result = await db.execute(stmt)
    await db.commit()
    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )
    return {"message":"deleted"}, 200

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

    
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from exceptions.exceptions import ConflictException, NotFoundException
# from models.employee import Employee
from sqlalchemy.exc import IntegrityError
from fastapi import status
from datetime import datetime
from models.department import Department
from models.employee import Address
from sqlalchemy.orm import selectinload
from models.employee import Employee
import logging

logger = logging.getLogger(__name__)

async def create(name:str, email:str, age:int, password_hash: str, db: AsyncSession) -> Employee:
    db_employee = Employee(name=name.strip(), email=email.strip(), age=age, password_hash=password_hash)
    db.add(db_employee)
    try:
        await db.commit()
        logger.info(f"Username: {name}, Email: {email} - Get Created")
    except IntegrityError:
        await db.rollback()
        raise ConflictException(detail=f"Email '{email.strip()}' is already in use")
    await db.refresh(db_employee)
    return db_employee

async def get_all_employee(db: AsyncSession):
    stmt = select(Employee).where(Employee.deleted_at.is_(None))
    result = await db.scalars(stmt)
    return result

async def get_employee_by_id(db: AsyncSession, employee_id: int) -> Employee:
    stmt = select(Employee).where(Employee.deleted_at.is_(None), Employee.id == employee_id)
    result = await db.scalar(stmt)
    return result
                 

async def get_by_email(email: str, db: AsyncSession):
    stmt = select(Employee).where(Employee.email == email)
    result = await db.scalars(stmt)
    return result.first()

async def update_employee(
    employee_id: int,
    name: str,
    email: str,
    age: int,
    db: AsyncSession
):
    employee = await get_employee_by_id(
        db=db,
        employee_id=employee_id
    )

    if employee is None:
        return None

    employee.name = name.strip()
    employee.email = email.strip()
    employee.age = age

    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{email}' already exists"
        ) from exc

    await db.refresh(employee)

    return employee

async def patch_employee(
    employee_id: int,
    data: dict,
    db: AsyncSession
):
    employee = await get_employee_by_id(
        db=db,
        employee_id=employee_id
    )

    if employee is None:
        return None

    for key, value in data.items():
        setattr(employee, key, value)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException(detail="Email already exists")

    await db.refresh(employee)

    return employee

async def delete_employee(
    employee_id: int,
    db: AsyncSession
):
    employee = await get_employee_by_id(
        db=db,
        employee_id=employee_id
    )

    if employee is None:
        return None

    employee.deleted_at = datetime.utcnow()

    await db.commit()

    return employee





async def attach_department(
    employee_id: int,
    department_id: int,
    db: AsyncSession
):
    stmt = (
        select(Employee)
        .options(
            selectinload(Employee.departments)
        )
        .where(Employee.id == employee_id)
    )

    employee = await db.scalar(stmt)

    if employee is None:
        return None, "employee"

    department = await db.get(
        Department,
        department_id
    )

    if department is None:
        return None, "department"

    if department not in employee.departments:
        employee.departments.append(
            department
        )

    await db.commit()

    await db.refresh(employee)

    return employee, None


async def detach_department(
    employee_id: int,
    department_id: int,
    db: AsyncSession
):
    stmt = (
        select(Employee)
        .options(
            selectinload(Employee.departments)
        )
        .where(Employee.id == employee_id)
    )

    employee = await db.scalar(stmt)

    if employee is None:
        raise NotFoundException(detail="Employee not found")
        # return None, "employee"

    department = await db.get(
        Department,
        department_id
    )

    if department is None:
        raise NotFoundException(detail="Department not found")
        # return None, "department"

    if department in employee.departments:
        employee.departments.remove(
            department
        )

    await db.commit()

    await db.refresh(employee)

    return employee, None

async def delete_employee_address(
    employee_id: int,
    address_id: int,
    db: AsyncSession
):
    employee = await db.get(
        Employee,
        employee_id
    )

    if employee is None:
        raise NotFoundException(detail="Employee not found")

    address = await db.get(
        Address,
        address_id
    )

    if address is None:
        raise NotFoundException(detail="Address not found")

    if address.employee_id != employee.id:
        return None, "ownership"

    await db.delete(address)

    await db.commit()

    return True, None


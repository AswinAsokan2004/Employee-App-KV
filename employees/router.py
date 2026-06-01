from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from auth.dependancies import get_current_user, require_role
from auth.schema import LoginResponse, TokenPayload
from database.connection import get_db
from employees import employee_services
from employees.schemas import EmployeeCreate, EmployeePatch, EmployeeResponds, EmployeeGetByIDResponds, EmployeeUpdate, MessageResponds, loginRequest, loginResponds
from exceptions.exceptions import UnAutherizedException
from auth.utils import (
    verify_token,
    create_access_token
)

from employees.schemas import (
    RefreshTokenRequest
)

from fastapi.security import OAuth2PasswordRequestForm

from models.employee import EmployeeRole

router = APIRouter(prefix='/employee')

@router.post("/create", status_code=status.HTTP_201_CREATED, tags=["Employees"], response_model=list[EmployeeResponds])
async def create(body: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    name = body.name
    email = body.email
    age = body.age
    password = body.password
    result = await employee_services.create(name=name, email=email, age=age, password=password, db=db)
    return [result]

# @router.get("/get", status_code=status.HTTP_200_OK, tags=["Employees"], response_model=list[EmployeeGetByIDResponds])
# async def get_all_employees(db: AsyncSession = Depends(get_db)):
#     result = await employee_services.get_all_employee(db=db)
#     return result

@router.get("/get", response_model=list[EmployeeGetByIDResponds], dependencies=[Depends(require_role(EmployeeRole.HR))])
async def get_all_employees(
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):  
    print(f"Current user :  {_current_user}")
    return await employee_services.get_all_employee(db)

@router.get("/get/{id}", status_code=status.HTTP_200_OK, tags=["Employees"], response_model=EmployeeGetByIDResponds)
async def get_all_employees_by_id(id: int, db: AsyncSession = Depends(get_db), _current_user: TokenPayload =Depends(get_current_user)):
    print(f"employee id = {id}")
    result = await employee_services.get_employee_by_id(db=db, employee_id=id)
    return result

@router.put(
    "/update/{id}",
    status_code=status.HTTP_200_OK,
    tags=["Employees"],
    response_model=EmployeeUpdate
)
async def update_employee(
    id: int,
    body: EmployeeUpdate,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user)
):
    return await employee_services.update_employee(
        employee_id=id,
        name=body.name,
        email=body.email,
        age=body.age,
        db=db
    )

@router.patch(
    "/patch/{id}",
    status_code=status.HTTP_200_OK,
    tags=["Employees"],
    response_model=EmployeePatch
)
async def patch_employee(
    id: int,
    body: EmployeePatch,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user)
):
    data = body.model_dump(exclude_unset=True)

    return await employee_services.patch_employee(
        employee_id=id,
        data=data,
        db=db
    )

@router.delete(
    "/delete/{id}",
    status_code=status.HTTP_200_OK,
    tags=["Employees"]
)
async def delete_employee(
    id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await employee_services.delete_employee(
        employee_id=id,
        db=db
    )
    

# @router.post("/login", status_code=status.HTTP_200_OK, tags=['Employees']) #response_model=loginResponds
# async def login_email(body:loginRequest, db: AsyncSession = Depends(get_db)):
#     email = body.email
#     password = body.password
#     result = await employee_services.get_by_email(db=db, email=email, password=password)
#     return {"token":result}


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse,
    tags=["Employees"]
)
async def login_email(
    # body: loginRequest,
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user)
):
    return await employee_services.get_by_email(
        db=db,
        # email=body.email,
        # password=body.password
        email = form.username,
        password = form.password
    )

@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    tags=["Employees"]
)
async def refresh_access_token(
    body: RefreshTokenRequest,
    _current_user: TokenPayload = Depends(get_current_user)
):
    payload = verify_token(
        body.refresh_token
    )

    if payload is None:
        raise UnAutherizedException(detail="Invalid refresh token")

    if payload.get("type") != "refresh":
        raise UnAutherizedException(detail="Invalid token type")

    new_payload = {
        "sub": payload.get("sub"),
        "email": payload.get("email"),
        "role": payload.get("role")
    }

    new_access_token = create_access_token(
        data=new_payload
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }

@router.post(
    "/{employee_id}/departments/{department_id}",
    response_model=MessageResponds
)
async def attach_department(
    employee_id: int,
    department_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user)
):
    return await employee_services.attach_department(
        employee_id=employee_id,
        department_id=department_id,
        db=db
    )

@router.delete(
    "/{employee_id}/departments/{department_id}",
    response_model=MessageResponds
)
async def detach_department(
    employee_id: int,
    department_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user)
):
    return await employee_services.detach_department(
        employee_id=employee_id,
        department_id=department_id,
        db=db
    )


@router.delete(
    "/{employee_id}/addresses/{address_id}",
    response_model=MessageResponds

)
async def delete_employee_address(
    employee_id: int,
    address_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user)
):
    return await employee_services.delete_employee_address(
        employee_id=employee_id,
        address_id=address_id,
        db=db
    )


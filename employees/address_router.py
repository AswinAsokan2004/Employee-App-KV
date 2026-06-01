from fastapi import APIRouter, Depends

from auth.dependancies import get_current_user
from auth.schema import TokenPayload
from database.connection import get_db
from employees import address_services
from employees.address_schemas import (
    AddressCreate,
    AddressResponse,
    AddressUpdate,
    AddressPatch
)
from sqlalchemy.ext.asyncio import AsyncSession

from employees.schemas import MessageResponds

router_address = APIRouter(
    prefix="/address",
    tags=["Address"]
)

@router_address.post("/address/create/{employee_id}", response_model=AddressResponse)
async def create_address(
    employee_id: int,
    body: AddressCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await address_services.create(
        employee_id=employee_id,
        line1=body.line1,
        city=body.city,
        postal_code=body.postal_code,
        country=body.country,
        db=db
    )

@router_address.get("/address/get", tags=['Address'], response_model=list[AddressResponse])
async def get_all_addresses(
    db: AsyncSession = Depends(get_db)
):
    return await address_services.get_all(
        db=db
    )

@router_address.get("/address/get/{id}", tags=['Address'], response_model=AddressResponse)
async def get_address_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await address_services.get_by_id(
        address_id=id,
        db=db
    )

@router_address.get("/address/get/employee/{employee_id}", tags=['Address'], response_model=list[AddressResponse])
async def get_employee_addresses(
    employee_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await address_services.get_by_employee_id(
        employee_id=employee_id,
        db=db
    )

@router_address.put("/address/update/{id}", tags=['Address'], response_model=AddressResponse)
async def update_address(
    id: int,
    body: AddressUpdate,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await address_services.update(
        address_id=id,
        line1=body.line1,
        city=body.city,
        postal_code=body.postal_code,
        country=body.country,
        db=db
    )

@router_address.patch("/address/patch/{id}", tags=['Address'], response_model=AddressResponse)
async def patch_address(
    id: int,
    body: AddressPatch,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    data = body.model_dump(
        exclude_unset=True
    )

    return await address_services.patch(
        address_id=id,
        data=data,
        db=db
    )

@router_address.delete("/address/delete/{id}", tags=['Address'], response_model=MessageResponds)
async def delete_address(
    id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
    
):
    return await address_services.delete(
        address_id=id,
        db=db
    )
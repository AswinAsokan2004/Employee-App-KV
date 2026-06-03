from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependancies import get_current_user, require_role
from auth.schema import TokenPayload
from database.connection import get_db
from departments import department_services
from departments.schemas import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentPatch,
    DepartmentResponse,
    MessageResponds,
)
from models.employee import EmployeeRole

router_dep = APIRouter(prefix="/department", tags=["Departments"])


@router_dep.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=DepartmentResponse,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def create(
    body: DepartmentCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await department_services.create(name=body.name, db=db)


@router_dep.get(
    "/get", status_code=status.HTTP_200_OK, response_model=list[DepartmentResponse]
)
async def get_all(
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await department_services.get_all(db=db)


@router_dep.get(
    "/get/{id}", status_code=status.HTTP_200_OK, response_model=DepartmentResponse
)
async def get_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await department_services.get_by_id(department_id=id, db=db)


@router_dep.put(
    "/update/{id}",
    status_code=status.HTTP_200_OK,
    response_model=DepartmentResponse,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def update(
    id: int,
    body: DepartmentUpdate,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await department_services.update(department_id=id, name=body.name, db=db)


@router_dep.patch(
    "/patch/{id}",
    status_code=status.HTTP_200_OK,
    response_model=DepartmentResponse,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def patch(
    id: int,
    body: DepartmentPatch,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    data = body.model_dump(exclude_unset=True)

    return await department_services.patch(department_id=id, data=data, db=db)


@router_dep.delete(
    "/delete/{id}",
    status_code=status.HTTP_200_OK,
    response_model=MessageResponds,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def delete(
    id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await department_services.delete(department_id=id, db=db)

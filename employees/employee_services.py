from fastapi import HTTPException
from fastapi import status
from auth.utils import create_access_token, hash_password, verify_password
from employees import employee_repo
from sqlalchemy.ext.asyncio import AsyncSession

from employees import address_services
from exceptions.exceptions import NotFoundException
from auth.utils import create_refresh_token


async def create(
    name: str, email: str, age: int, password: str, address: dict, db: AsyncSession
):
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

    password_hashed = hash_password(password)
    employee = await employee_repo.create(
        name=name, email=email, age=age, password_hash=password_hashed, db=db
    )
    address_list = None
    if address is not None:
        address_list = await address_services.create(
            employee_id=employee.id,
            line1=address.line1,
            city=address.city,
            postal_code=address.postalcode,
            country=address.country,
            db=db,
        )
    return employee, address_list


async def get_all_employee(db: AsyncSession):
    result = await employee_repo.get_all_employee(db=db)
    return [r.to_api_dict() for r in result.all()]


async def get_employee_by_id(employee_id: int, db: AsyncSession):
    result = await employee_repo.get_employee_by_id(employee_id=employee_id, db=db)
    # try:
    if not result:
        raise NotFoundException(
            detail="Employee of employee id {employee_id} Not Found : try again with valid id".format(
                employee_id=employee_id
            )
        )  # HTTPException(status_code=404, detail="Employee not found")
    return result.to_api_dict()
    # except NotFoundException as e:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


# async def get_by_email(email: str, password: str, db: AsyncSession):
#     employee = await employee_repo.get_by_email(email=email, db=db)
#     if employee is None:
#         raise NotFoundException(detail="No employee found from repo")

#     if not verify_password(plain=password.strip(),hashed=employee.password_hash):
#         raise NotFoundException(detail="Password Verification failed in services")


#     data_body = {"email":email, "password":password}
#     result = create_access_token(data=data_body)
#     return result
async def get_by_email(email: str, password: str, db: AsyncSession):
    employee = await employee_repo.get_by_email(email=email, db=db)

    if employee is None:
        raise NotFoundException(detail="Employee not found")

    if not verify_password(plain=password.strip(), hashed=employee.password_hash):
        raise NotFoundException(detail="Invalid password")

    payload = {
        "sub": str(employee.id),
        "email": employee.email,
        "role": employee.role.value,
    }

    access_token = create_access_token(data=payload)

    refresh_token = create_refresh_token(data=payload)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


async def update_employee(
    employee_id: int, name: str, email: str, age: int, db: AsyncSession
):
    employee = await employee_repo.update_employee(
        employee_id=employee_id, name=name, email=email, age=age, db=db
    )

    if employee is None:
        raise NotFoundException(detail="Employee not found")

    return employee.to_api_dict()


async def patch_employee(employee_id: int, data: dict, db: AsyncSession):
    employee = await employee_repo.patch_employee(
        employee_id=employee_id, data=data, db=db
    )

    if employee is None:
        raise NotFoundException(detail="Employee not found")

    return employee.to_api_dict()


async def delete_employee(employee_id: int, db: AsyncSession):
    employee = await employee_repo.delete_employee(employee_id=employee_id, db=db)

    if employee is None:
        raise NotFoundException(detail="Employee not found")

    return {"message": f"Employee {employee_id} deleted successfully"}


async def attach_department(employee_id: int, department_id: int, db: AsyncSession):
    result, error = await employee_repo.attach_department(
        employee_id=employee_id, department_id=department_id, db=db
    )

    if error == "employee":
        raise NotFoundException(detail="Employee not found")

    if error == "department":
        raise NotFoundException(detail="Department not found")

    return {"message": "Department attached successfully"}


async def detach_department(employee_id: int, department_id: int, db: AsyncSession):
    result, error = await employee_repo.detach_department(
        employee_id=employee_id, department_id=department_id, db=db
    )

    if error == "employee":
        raise NotFoundException(detail="Employee not found")

    if error == "department":
        raise NotFoundException(detail="Department not found")

    return {"message": "Department detached successfully"}


async def delete_employee_address(employee_id: int, address_id: int, db: AsyncSession):
    result, error = await employee_repo.delete_employee_address(
        employee_id=employee_id, address_id=address_id, db=db
    )

    if error == "employee":
        raise NotFoundException(detail="Employee not found")

    if error == "address":
        raise NotFoundException(detail="Address not found")

    if error == "ownership":
        raise NotFoundException(detail="Address does not belong to employee")

    return {"message": "Address deleted successfully"}


async def get_employee_departments(employee_id: int, db: AsyncSession):
    result = await employee_repo.get_employee_departments(
        employee_id=employee_id, db=db
    )

    if result is None:
        raise NotFoundException(detail="Employee not found")

    return result  # [department.name for department in result]

from fastapi import status
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from auth.schema import LoginResponse
from database.connection import get_db
from employees import employee_services
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from auth.utils import hash_password

logger = logging.getLogger(__name__)
router_auth = APIRouter(prefix="/auth", tags=["Auth"])


@router_auth.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse,
    tags=["Employees"],
)
async def login_email(
    # body: loginRequest,
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    result = await employee_services.get_by_email(
        db=db, email=form.username, password=form.password
    )
    logger.info(
        f"Logged : {form.username} - password : {hash_password(form.password)[:8]}"
    )
    return result

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from auth.schema import TokenPayload
from auth.utils import decode_access_token
from models.employee import EmployeeRole


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_schema)):
    payload = decode_access_token(token=token)
    if payload is None:
        raise Exception("User unable to access")
    return payload

# print(get_current_user(token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0NCIsImVtYWlsIjoiQXZ2ZGRzZHNlMzNhc3FkQGdtYWlsLmNvbSIsImV4cCI6MTc4MDI5MTY2OCwidHlwZSI6ImFjY2VzcyJ9.7jcqG22-JGK066GD1odiOBNKFbIvMhN1EUCqMlkr3Dk"))

# print(get_current_user(token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0NCIsImVtYWlsIjoiQXZ2ZGRzZHNlMzNhc3FkQGdtYWlsLmNvbSIsImV4cCI6MTc4MDg5Mjg2OCwidHlwZSI6InJlZnJlc2gifQ.rRkEmj7F2YBHwUHMhhfmyww09dRGsjGqkKZB5uVpEiE"))

def require_role(required_role: EmployeeRole):

    def role_checker(
        current_user: TokenPayload = Depends(get_current_user),
    ):
        print(current_user)
        if current_user.get("role") != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )

        return current_user

    return role_checker
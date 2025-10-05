from fastapi import Depends, HTTPException, status
from utils.security import get_current_user
import models

def require_role(roles: list[str]):
    def role_checker(current_user: models.User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = "Acesso negado."
            )
        return current_user
    return role_checker

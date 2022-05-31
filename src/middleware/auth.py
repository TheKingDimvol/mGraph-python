from typing import Optional
from fastapi import Header, HTTPException
from starlette import status

from src.controllers.auth import AuthController


def get_current_user(token: Optional[str] = Header(None)):
    if not token:
        # Enable/disable authentication
        return None
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Need token authentication for this request!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return AuthController.validate_token(token)

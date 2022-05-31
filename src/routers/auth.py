from fastapi import APIRouter

from src.controllers.auth import AuthController
from src.schemas.auth import UserCredentials, TokenData


router = APIRouter(prefix='/auth', tags=['Authorization'])


@router.post("/login", response_model=dict)
def login(user_data: UserCredentials):
    return AuthController.login(user_data)


@router.post("/signup", response_model=TokenData)
def signup(user_data: UserCredentials):
    return AuthController.signup(user_data)

from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import jwt, JWTError
from passlib.hash import bcrypt

from db_object_classes.user import User
from src.schemas.auth import TokenData
from src.settings import settings


class AuthController:
    """Класс для операций, связанных с авторизацией
    """

    @classmethod
    def login(cls, credentials):
        user = User.find(username=credentials.username)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User doesn't exist!",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not cls.verify_password(credentials.password, user.get('password')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Wrong password!",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = cls.create_token({
            'username': user.get('username'),
            'uuid': user.get('uuid')
        })

        user.pop('password')
        return {**token.dict(), **user}

    @classmethod
    def signup(cls, user):
        if not user.username or not user.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Username and password are required!",
                headers={"WWW-Authenticate": "Bearer"},
            )

        existing_user = User.find(username=user.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Username "{user.username}" is taken!',
                headers={"WWW-Authenticate": "Bearer"},
            )

        user.password = cls.hash_password(user.password)

        user = User.create(**user.dict())

        return cls.create_token({
            'username': user.get('username'),
            'uuid': user.get('uuid')
        })

    @staticmethod
    def verify_password(plain_password: str, hashed_password) -> bool:
        try:
            return bcrypt.verify(plain_password, hashed_password)
        except ValueError:
            return False

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hash(password)

    @staticmethod
    def validate_token(token: str):
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm]
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload.get('user') or None

    @staticmethod
    def create_token(user: dict) -> TokenData:
        now = datetime.now()

        payload = {
            'iat': now,
            'nbf': 0,
            'exp': now + timedelta(seconds=settings.jwt_expiration),
            'sub': str(user['uuid']),
            'user': user
        }

        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm
        )

        return TokenData(access_token=token)

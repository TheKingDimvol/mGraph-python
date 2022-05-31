from typing import Optional

from fastapi import APIRouter, HTTPException, status, Depends

from controllers.type import TypeController
from middleware.auth import get_current_user
from schemas.type import TypeCreateModel

router = APIRouter(prefix='/types', tags=['Types'])


@router.get('/')
def home_page():
    return 'Type route'


@router.post('/')
def create_type(typology_data: TypeCreateModel, curr_user: dict = Depends(get_current_user)):
    return TypeController.create(typology_data)


@router.get('/{uuid}')
def read_type(uuid: str, typology: Optional[str] = None, curr_user: dict = Depends(get_current_user)):
    if uuid == 'all':
        if typology is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Need to clarify typology to get all types!',
                headers={"WWW-Authenticate": "Bearer"},
            )
        return TypeController.read_all(typology)
    return TypeController.read(uuid)


@router.delete('/{uuid}')
def delete_type(uuid: str, curr_user: dict = Depends(get_current_user)):
    return TypeController.delete(uuid)

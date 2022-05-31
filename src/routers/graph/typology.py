from fastapi import APIRouter, Depends

from controllers.typology import TypologyController
from middleware.auth import get_current_user
from schemas.typology import TypologyCreateModel

router = APIRouter(prefix='/typologies', tags=['Typologies'])


@router.get('/')
def home_page():
    return 'Typology route'


@router.post('/')
def create_typology(typology_data: TypologyCreateModel, curr_user: dict = Depends(get_current_user)):
    return TypologyController.create(typology_data)


@router.get('/{uuid}')
def read_typology(uuid: str, curr_user: dict = Depends(get_current_user)):
    if uuid == 'all':
        return TypologyController.read_all_typologies()
    return TypologyController.read(uuid)


@router.delete('/{uuid}')
def delete_typology(uuid: str, curr_user: dict = Depends(get_current_user)):
    return TypologyController.delete(uuid)

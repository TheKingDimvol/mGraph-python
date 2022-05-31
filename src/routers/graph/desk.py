from fastapi import APIRouter, Depends

from controllers.desk import DeskController
from middleware.auth import get_current_user
from schemas.desk import DeskCreateModel

router = APIRouter(prefix='/desks', tags=['Desks'])


@router.get('/')
def home_page():
    return 'Desk route'


@router.post('/')
def create_desk(typology_data: DeskCreateModel, curr_user: dict = Depends(get_current_user)):
    return DeskController.create(typology_data)


@router.get('/{uuid}')
def read_desk(uuid: str, curr_user: dict = Depends(get_current_user)):
    if uuid == 'all':
        return DeskController.read_all_desks()
    return DeskController.read(uuid)


@router.delete('/{uuid}')
def delete_desk(uuid: str, curr_user: dict = Depends(get_current_user)):
    return DeskController.delete(uuid)

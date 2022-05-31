from fastapi import APIRouter, Depends

from controllers.relationship import RelationshipController
from middleware.auth import get_current_user
from schemas.relationship import RelationshipCreateModel

router = APIRouter(prefix='/edges', tags=['Edges'])


@router.get('/')
def home_page():
    return 'Relationship route'


@router.post('/')
def rs_create(rs_data: RelationshipCreateModel, curr_user: dict = Depends(get_current_user)):
    return RelationshipController.create(rs_data)


@router.get('/{uuid}')
def rs_read(
        desk: str = None, typology: str = None,
        start: str = None, end: str = None,
        uuid: str = None):
    return RelationshipController.read(desk=desk, typology=typology, start=start, end=end, uuid=uuid)


@router.delete('/{uuid}')
def rs_delete(uuid: str, curr_user: dict = Depends(get_current_user)):
    return RelationshipController.delete(uuid)

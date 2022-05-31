from typing import Optional

from fastapi import APIRouter, HTTPException, status, Depends

from controllers.node import NodeController
from controllers.websocket import manager
from middleware.auth import get_current_user
from schemas.node import NodeCreateModel


router = APIRouter(prefix='/nodes', tags=['Nodes'])


@router.get('/')
def home_page():
    return 'Node route'


@router.post('/')
async def create_node(node_data: NodeCreateModel, curr_user: dict = Depends(get_current_user)):
    node = NodeController.create(node_data)
    await manager.graph_changed(node_data.desk_uuid, new_nodes=[node])
    return node


@router.get('/{uuid}')
def read_node(uuid: str, desk: Optional[str] = None, curr_user: dict = Depends(get_current_user)):
    if uuid == 'all':
        if desk is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Need to clarify desk to get all nodes!',
                headers={"WWW-Authenticate": "Bearer"},
            )
        return NodeController.read_all(desk)
    return NodeController.read(uuid)


@router.delete('/{uuid}')
async def delete_node(uuid: str, desk_uuid: str = None, curr_user: dict = Depends(get_current_user)):
    deleted = NodeController.delete(uuid)
    if desk_uuid:
        await manager.graph_changed(desk_uuid, deleted_nodes=[uuid])
    return deleted


@router.put('/{uuid}')
def update_node(uuid: str, curr_user: dict = Depends(get_current_user), **params):
    return uuid

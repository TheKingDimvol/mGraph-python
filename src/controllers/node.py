from fastapi import HTTPException, status

from constants import EdgeLabels
from db_object_classes.desk import Desk
from db_object_classes.node import Node
from db_object_classes.relationship import Relationship
from db_object_classes.type import Type


class NodeController:
    @classmethod
    def create(cls, node_data):
        desk = Desk.read(desk_uuid=node_data.desk_uuid)
        if not desk:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Such desk does not exist!",
                headers={"WWW-Authenticate": "Bearer"},
            )

        _type = Type.read(node_uuid=node_data.type_uuid)
        if not _type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Such desk does not exist!",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not Type.type_from_desk_or_typology(node_data.type_uuid, node_data.desk_uuid):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Type does not belong to current typology!",
                headers={"WWW-Authenticate": "Bearer"},
            )

        new_node = None

        try:
            new_node = Node.create(
                title=node_data.title,
                type_title=_type['label'],
                desk_uuid=desk['uuid'],
                **node_data.params
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"},
            )

        relationship = Relationship.create(node_data.desk_uuid, new_node.get('uuid'), EdgeLabels.Owns)

        return new_node

    @classmethod
    def read(cls, uuid):
        return Node.read(node_uuid=uuid)

    @classmethod
    def read_all(cls, desk_uuid):
        return Desk.get_nodes(desk_uuid)

    @classmethod
    def delete(cls, uuid):
        return Node.delete(node_uuid=uuid)

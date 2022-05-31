from fastapi import HTTPException, status

from db_object_classes.desk import Desk
from db_object_classes.node import Node
from db_object_classes.relationship import Relationship
from db_object_classes.type import Type
from schemas.relationship import RelationTypeEnum


class RelationshipController:
    @classmethod
    def create(cls, rs_data):
        object_class = Node if rs_data.type == RelationTypeEnum.node else Type

        start = object_class.read(node_uuid=rs_data.start)
        if not start:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Start {rs_data.type} does not exist!",
                headers={"WWW-Authenticate": "Bearer"},
            )

        end = object_class.read(node_uuid=rs_data.end)
        if not end:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"End {rs_data.type} does not exist!",
                headers={"WWW-Authenticate": "Bearer"},
            )

        new_rs = None

        try:
            new_rs = Relationship.create(rs_data.start, rs_data.end, rs_data.title, **rs_data.params)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"},
            )

        return new_rs

    @classmethod
    def read(cls, **params):
        uuid = params.get('uuid')
        if uuid:
            if uuid == 'all':
                if params.get('desk'):
                    return Relationship.read_all(params['desk'], True)

                elif params.get('typology'):
                    return Relationship.read_all(params['typology'], False)

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Need desk or typology uuid for all edges!',
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return Relationship.read(relation_uuid=uuid)

        elif 'start' in params and 'end' in params:
            return Relationship.read(first_node_uuid=params['start'], second_node_uuid=params['end'])

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Edges UUID, or start and end node, or desk or typology are not provided!',
            headers={"WWW-Authenticate": "Bearer"},
        )

    @classmethod
    def delete(cls, uuid):
        return Relationship.delete(relation_uuid=uuid)

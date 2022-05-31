from fastapi import HTTPException, status

from constants import EdgeLabels
from db_object_classes.desk import Desk
from db_object_classes.relationship import Relationship
from db_object_classes.typology import Typology


class DeskController:
    @classmethod
    def create(cls, desk_data):
        # Доска может использовать как типологию напрямую, так и через другую доску
        if not Typology.read(node_uuid=desk_data.typology_uuid) and not Desk.read(node_uuid=desk_data.typology_uuid):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Such typology does not exist!",
                headers={"WWW-Authenticate": "Bearer"},
            )

        new_desk = None

        try:
            new_desk = Desk.create(title=desk_data.title, **desk_data.params)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"},
            )

        relationship = Relationship.create(new_desk.get('uuid'), desk_data.typology_uuid, EdgeLabels.Using)

        return new_desk

    @classmethod
    def read_all_desks(cls):
        return Desk.read_all()

    @classmethod
    def read(cls, uuid):
        return Desk.read(desk_uuid=uuid)

    @classmethod
    def delete(cls, uuid):
        return Desk.delete(node_uuid=uuid)

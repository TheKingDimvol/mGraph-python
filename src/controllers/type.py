from fastapi import HTTPException, status

from constants import EdgeLabels
from db_object_classes.relationship import Relationship
from db_object_classes.type import Type
from db_object_classes.typology import Typology


class TypeController:
    @classmethod
    def create(cls, type_data):
        typology = Typology.read(node_uuid=type_data.typology_uuid)
        if not typology:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Such typology does not exist!",
                headers={"WWW-Authenticate": "Bearer"},
            )

        new_type = None

        try:
            new_type = Type.create(title=type_data.title, community=typology.get('types_count'), **type_data.params)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"},
            )

        relationship = Relationship.create(type_data.typology_uuid, new_type.get('uuid'), EdgeLabels.Owns)

        return new_type

    @classmethod
    def read_all(cls, typology_uuid):
        return Typology.get_types(typology_uuid=typology_uuid)

    @classmethod
    def read(cls, uuid):
        return Type.read(node_uuid=uuid)

    @classmethod
    def delete(cls, uuid):
        return Type.delete(node_uuid=uuid)

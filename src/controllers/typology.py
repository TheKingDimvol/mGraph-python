from db_object_classes.typology import Typology


class TypologyController:
    @classmethod
    def create(cls, typology_data):
        return Typology.create(title=typology_data.title, **typology_data.params)

    @classmethod
    def read(cls, uuid):
        return Typology.read(node_uuid=uuid)

    @classmethod
    def read_all_typologies(cls):
        return Typology.read_all()

    @classmethod
    def delete(cls, uuid):
        return Typology.delete(node_uuid=uuid)

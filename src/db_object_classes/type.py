from constants import NodeLabels, EdgeLabels
from db_object_classes.base_node import BaseNode


class Type(BaseNode):
    type = NodeLabels.Type

    @classmethod
    def create(cls, **params):
        return super().create(**params)

    @classmethod
    def type_from_desk_or_typology(cls, type_uuid, typology_uuid):
        """
        Проверка на то, что тип принадлежит типологии или доске
        :param type_uuid: UUID типа
        :param typology_uuid: UUID типологии или доски
        :return: принадлежность типа типологии/доске
        """
        return cls.execute_query_single(
            f'MATCH (d:{NodeLabels.Desk})-[*0..{{type: \'{EdgeLabels.Using}\'}}]->(t:{NodeLabels.Typology})'
            f'-[{{type: \'{EdgeLabels.Owns}\'}}]->(:{NodeLabels.Type} {{uuid: "{type_uuid}"}}) '
            f'WHERE d.uuid = "{typology_uuid}" OR t.uuid = "{typology_uuid}" '
            f'RETURN TRUE'
        )

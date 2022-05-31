from constants import NodeLabels, EdgeLabels
from db_object_classes.base_node import BaseNode


TYPE_RETURN_FIELDS = 'ID(type) AS id, LABELS(type) AS labels, type AS params'

TYPOLOGY_RETURN_FIELDS = 'ID(typology) AS id, LABELS(typology) AS labels, typology AS params'


class Typology(BaseNode):
    type = NodeLabels.Typology

    _typology_types_query = f'MATCH (typology:{NodeLabels.Typology})<-[*0..{{{{type: \'{EdgeLabels.Using}\'}}}}]-(:{NodeLabels.Typology})' \
                            f'-[{{{{type: \'{EdgeLabels.Owns}\'}}}}]->(type:{NodeLabels.Type}) {{condition}} ' \
                            f'RETURN ' + TYPE_RETURN_FIELDS

    _all_typologies = f"""
        // Типологии с досками и типами
        MATCH (type:{NodeLabels.Type})<-[{{type: '{EdgeLabels.Owns}'}}]-(:{NodeLabels.Typology})
        -[*0..{{type: '{EdgeLabels.Using}'}}]-(typology:{NodeLabels.Typology})
        <-[*0..{{type: '{EdgeLabels.Using}'}}]-(desk:{NodeLabels.Desk})
        RETURN {TYPOLOGY_RETURN_FIELDS}, count(DISTINCT type) AS types, count(DISTINCT desk) AS desks
        UNION 
        // С типами, без досок
        MATCH (type:{NodeLabels.Type})<-[{{type: '{EdgeLabels.Owns}'}}]-(:{NodeLabels.Typology})
        -[*0..{{type: '{EdgeLabels.Using}'}}]-(typology:{NodeLabels.Typology})
        WHERE NOT (typology)<-[*0..{{type: '{EdgeLabels.Using}'}}]-(:{NodeLabels.Desk})
        RETURN {TYPOLOGY_RETURN_FIELDS}, count(DISTINCT type) AS types, 0 AS desks
        UNION 
        // С досками, без типов
        MATCH (typology:{NodeLabels.Typology})<-[*0..{{type: '{EdgeLabels.Using}'}}]-(desk:{NodeLabels.Desk})
        WHERE NOT (:{NodeLabels.Type})<-[{{type: '{EdgeLabels.Owns}'}}]-(:{NodeLabels.Typology})-[*0..{{type: '{EdgeLabels.Using}'}}]-(typology)
        RETURN {TYPOLOGY_RETURN_FIELDS}, 0 AS types, count(desk) AS desks
        UNION 
        // Без типов и без досок
        MATCH (typology:{NodeLabels.Typology})<-[*0..{{type: '{EdgeLabels.Using}'}}]-(desk:{NodeLabels.Desk})
        WHERE NOT (:{NodeLabels.Type})<-[{{type: '{EdgeLabels.Owns}'}}]-(:{NodeLabels.Typology})-[*0..{{type: '{EdgeLabels.Using}'}}]-(typology) AND NOT (typology)<-[*0..{{type: '{EdgeLabels.Using}'}}]-(:{NodeLabels.Desk})
        RETURN {TYPOLOGY_RETURN_FIELDS}, 0 AS types, 0 AS desks
    """

    @classmethod
    def create(cls, **params):
        if 'title' not in params:
            raise Exception('Нет обязательного поля title!')
        if not cls.is_title_unique(params['title']):
            raise Exception('Типология с таким название уже существует!')

        return super().create(**params)

    @classmethod
    def read(cls, node_id=None, node_uuid=None):
        typology = super().read(node_id, node_uuid)

        if typology:
            typology['types_count'] = cls.execute_query_single(
                f'MATCH '
                f'(typology:{NodeLabels.Typology} {{uuid: "{typology.get("uuid")}"}})-[{{type: \'{EdgeLabels.Owns}\'}}]->(type:{NodeLabels.Type}) '
                f'RETURN count(type) AS count'
            )['count']

        return typology

    @classmethod
    def read_all(cls):
        return cls.execute_query(cls._all_typologies)

    @classmethod
    def get_types(cls, typology_uuid):
        condition = f'WHERE typology.uuid = "{typology_uuid}"'
        return cls.execute_query(cls._typology_types_query.format(condition=condition))

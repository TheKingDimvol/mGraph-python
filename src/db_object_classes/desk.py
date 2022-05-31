from constants import EdgeLabels, NodeLabels
from src.db_object_classes.base_node import BaseNode


NODE_RETURN_FIELDS = 'ID(node) AS id, LABELS(node) AS labels, node AS params'
DESK_RETURN_FIELDS = 'ID(desk) AS id, LABELS(desk) AS labels, desk AS params'


class Desk(BaseNode):
    type = NodeLabels.Desk

    _read_query = f'MATCH (desk:{NodeLabels.Desk} {{{{uuid: "{{0}}" }}}})' \
                  f'-[*0..{{{{type: \'{EdgeLabels.Using}\'}}}}]->(:Desk)' \
                  f'-[{{{{type: \'{EdgeLabels.Using}\'}}}}]->(typology:{NodeLabels.Typology}) ' \
                  'RETURN typology.uuid AS typologyUuid, typology.title AS typologyTitle, ' + DESK_RETURN_FIELDS

    _all_desks = f"""
        // Доски с вершинами
        MATCH (node:{NodeLabels.Node})<-[{{type: '{EdgeLabels.Owns}'}}]-(:{NodeLabels.Desk})
        -[*0..{{type: '{EdgeLabels.Using}'}}]->(desk:{NodeLabels.Desk})
        -[*0..{{type: '{EdgeLabels.Using}'}}]->(typology:{NodeLabels.Typology})
        RETURN {DESK_RETURN_FIELDS}, typology.uuid AS typologyUuid, typology.title AS typologyTitle, count(DISTINCT node) AS nodes
        UNION
        // Пустые доски
        MATCH (desk:{NodeLabels.Desk})-[*0..{{type: '{EdgeLabels.Using}'}}]->(typology:{NodeLabels.Typology})
        WHERE NOT (:{NodeLabels.Node})<-[{{type: '{EdgeLabels.Owns}'}}]-(:{NodeLabels.Desk})-[*0..{{type: '{EdgeLabels.Using}'}}]->(desk)
        RETURN {DESK_RETURN_FIELDS}, typology.uuid AS typologyUuid, typology.title AS typologyTitle, 0 AS nodes
    """
    _desk_nodes_query = f'MATCH (desk:{NodeLabels.Desk})' \
                        f'<-[*0..{{{{type: \'{EdgeLabels.Using}\'}}}}]' \
                        f'-(:{NodeLabels.Desk})' \
                        f'-[{{{{type: \'{EdgeLabels.Owns}\'}}}}]' \
                        f'->(node:{NodeLabels.Node}) ' \
                        f'{{condition}} RETURN ' + NODE_RETURN_FIELDS

    @classmethod
    def create(cls, **params):
        if 'title' not in params:
            raise Exception('Нет обязательного поля title!')
        if not cls.is_title_unique(params['title']):
            raise Exception('Доска с таким названием уже существует!')

        return super().create(**params)

    @classmethod
    def read(cls, desk_id=None, desk_uuid=None):
        if not desk_uuid:
            raise Exception('Нужно передать UUID доски!')
        return cls.execute_query_single(cls._read_query.format(desk_uuid))

    @classmethod
    def read_all(cls):
        return cls.execute_query(cls._all_desks)

    @classmethod
    def get_nodes(cls, desk_uuid):
        condition = f'WHERE desk.uuid = "{desk_uuid}"'

        return cls.execute_query(cls._desk_nodes_query.format(condition=condition))

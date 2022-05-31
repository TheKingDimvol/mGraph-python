from constants import EdgeLabels, NodeLabels
from db_object_classes.base_node import BaseNode


class Node(BaseNode):
    type = NodeLabels.Node

    @classmethod
    def create(cls, **params):
        if 'type_title' not in params:
            raise Exception('Для создания вершины нужно передать название Типа!')
        if 'desk_uuid' not in params:
            raise Exception('Для создания вершины нужно передать UUID Доски!')

        desk_uuid = params.pop('desk_uuid')

        if not cls.is_title_unique(params['title'], desk_uuid):
            raise Exception('Вершина с таким названием уже существует в данной доске!')

        super().add_uuid(params)

        return cls.execute_query_single(
            cls._create_query.format(f':{cls.type}:`{params.pop("type_title")}`'), **params
        )

    @classmethod
    def is_title_unique(cls, title, desk_uuid):
        return not bool(cls.execute_query(
            f'MATCH (:{NodeLabels.Desk} {{uuid: "{desk_uuid}"}})'
            f'-[{{type: \'{EdgeLabels.Owns}\'}}]->(node:{cls.type} {{title: "{title}"}}) '
            f'RETURN TRUE'
        ))

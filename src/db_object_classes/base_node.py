from src.db_object_classes.base import Base


NODE_RETURN_FIELDS = 'ID(node) AS id, LABELS(node) AS labels, node AS params'


class BaseNode(Base):
    type = None

    _create_query = 'CREATE (node{0} $params) RETURN ' + NODE_RETURN_FIELDS

    _update_query = 'MATCH (node{0}) {1} SET node+=$params RETURN ' + NODE_RETURN_FIELDS

    _read_query = 'MATCH (node{0}) {1} RETURN ' + NODE_RETURN_FIELDS

    _delete_query = 'MATCH (node{0}) {1} DETACH DELETE node RETURN TRUE'  # Удалит вершину и все связи из нее

    @classmethod
    def insert_type(cls):
        return ':' + cls.type if cls.type else ''

    @classmethod
    def is_title_unique(cls, title):
        return not bool(cls.execute_query(
            f'MATCH (node:{cls.type} {{title: "{title}"}}) RETURN TRUE'
        ))

    @classmethod
    def create(cls, node_type=None, **params):
        super().add_uuid(params)
        if node_type is not None:
            node_type = f':{node_type}'
        elif cls.type:
            node_type = cls.insert_type()
        else:
            raise Exception('Не указан тип для создания вершины!')

        return cls.execute_query_single(
            cls._create_query.format(node_type), **params
        )

    @classmethod
    def update(cls, node_id=None, node_uuid=None, **params):
        if 'uuid' in params:
            del params['uuid']

        condition = cls.get_condition(node_id, node_uuid)
        if not condition:
            return None

        return cls.execute_query_single(
            cls._update_query.format(cls.insert_type(), condition),
            **params
        )

    @classmethod
    def get_all(cls):
        return cls.execute_query(
            f'MATCH (node{cls.insert_type()}) RETURN ' + NODE_RETURN_FIELDS
        )

    @classmethod
    def read(cls, node_id=None, node_uuid=None):
        condition = cls.get_condition(node_id, node_uuid)
        if not condition:
            return None

        return cls.execute_query_single(
            cls._read_query.format(cls.insert_type(), condition)
        )

    @classmethod
    def delete(cls, node_id=None, node_uuid=None):
        condition = cls.get_condition(node_id, node_uuid)
        if not condition:
            return False

        cls.execute_query_single(
            cls._delete_query.format(cls.insert_type(), condition)
        )
        return True

    @staticmethod
    def get_condition(node_id, node_uuid):
        condition = 'WHERE '
        if node_id is not None:
            condition += f'ID(node) = {node_id}'
        elif node_uuid:
            condition += f'node.uuid = "{node_uuid}"'
        else:
            return None  # TODO error
        return condition

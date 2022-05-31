from constants import NodeLabels
from db_object_classes.base_node import BaseNode


class User(BaseNode):
    type = NodeLabels.User

    @classmethod
    def create(cls, **params):
        return super().create(cls.type, **params)

    @classmethod
    def find(cls, username=None, _id=None, uuid=None):
        condition = None
        if username:
            condition = f'WHERE node.username = "{username}"'
        else:
            condition = cls.get_condition(_id, uuid)

        if not condition:
            raise Exception('Нужно передать логин, ID или UUID для поиска пользователя!')

        return cls.execute_query_single(
            cls._read_query.format(':' + cls.type, condition)
        )

    @classmethod
    def delete(cls, typology_uuid=None, **params):
        return super().create(**params)

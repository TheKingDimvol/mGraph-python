from constants import EdgeLabels
from src.db_object_classes.base import Base


RELATION_RETURN_FIELDS = '''
    PROPERTIES(relation) AS params, 
    TYPE(relation) AS type,
    STARTNODE(relation).title AS startTitle,
    ENDNODE(relation).title AS endTitle,
    STARTNODE(relation).uuid AS start,
    ENDNODE(relation).uuid AS end
'''


class Relationship(Base):
    _create_query = '''
        MATCH (start {{uuid: "{0}"}})
        MATCH (end {{uuid: "{1}"}})
        CREATE (start)-[relation:{2} $params]->(end)
        RETURN 
    ''' + RELATION_RETURN_FIELDS

    _update_query = 'MATCH (node{0}) SET {1}  WHERE {2} RETURN '

    _read_query = '''
        MATCH ({0})-[relation{1}]-({2}) 
        RETURN DISTINCT 
    ''' + RELATION_RETURN_FIELDS

    _read_all = '''
        MATCH (:{desk_type} {{uuid: "{uuid}"}})-[{{type: "''' + EdgeLabels.Owns + '''"}}]->(:{node_type})-[relation]->(:{node_type})
        RETURN 
    ''' + RELATION_RETURN_FIELDS

    _delete_query = 'MATCH ({0})-[relation{1}]-({2}) DELETE relation RETURN TRUE'

    @classmethod
    def create(cls, start_uuid, end_uuid, relation_type='СВЯЗАН_С', **params):
        super().add_uuid(params)
        params['type'] = relation_type
        return cls.execute_query_single(
            cls._create_query.format(
                start_uuid, end_uuid, relation_type
            ), **params
        )

    @classmethod
    def read(cls, first_node_uuid=None, second_node_uuid=None, relation_uuid=None, relation_type=None):
        result = cls.execute_query_single(
            cls._read_query.format(
                cls.match_condition(
                    first_node_uuid, second_node_uuid,
                    relation_uuid, relation_type
                )
            )
        )
        return result[0] if result else None

    @classmethod
    def read_all(cls, desk_uuid, for_desk=True):
        desk_type = 'Desk' if for_desk else 'Typology'
        node_type = 'Node' if for_desk else 'Type'

        return cls.execute_query(
            cls._read_all.format(uuid=desk_uuid, desk_type=desk_type, node_type=node_type)
        )

    @classmethod
    def delete(cls, first_node_uuid=None, second_node_uuid=None, relation_uuid=None, relation_type=None):
        cls.execute_query_single(
            cls._delete_query.format(
                cls.match_condition(
                    first_node_uuid, second_node_uuid,
                    relation_uuid, relation_type
                )
            )
        )
        return True

    @staticmethod
    def match_condition(first_node_uuid=None, second_node_uuid=None, relation_uuid=None, relation_type=None):
        rel_clause = ''
        if relation_type:
            rel_clause += f':{relation_type}'
        if relation_uuid:
            rel_clause += f' {{uuid: "{relation_uuid}"}}'

        first_node_clause = ''
        if first_node_uuid:
            first_node_clause = f'{{uuid: "{first_node_uuid}"}}'
        second_node_clause = ''
        if second_node_uuid:
            second_node_clause = f'{{uuid: "{second_node_uuid}"}}'
        return first_node_clause, rel_clause, second_node_clause

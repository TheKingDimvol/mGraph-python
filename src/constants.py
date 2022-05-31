from enum import Enum


NODE_TYPE_NAMES = [
    'Node', 'Type', 'Desk', 'Typology', 'User'
]


class NodeLabels(str, Enum):
    Typology = 'Typology'
    Type = 'Type'
    Desk = 'Desk'
    Node = 'Node'
    User = 'User'


class EdgeLabels(str, Enum):
    Using = 'ИСПОЛЬЗУЕТ'
    Owns = 'СОДЕРЖИТ'

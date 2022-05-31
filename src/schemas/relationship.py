from enum import Enum

from pydantic import BaseModel
from typing import Dict, Optional


class RelationTypeEnum(str, Enum):
    node = 'node'
    type = 'type'


class RelationshipCreateModel(BaseModel):
    title: str
    start: str
    end: str
    type: RelationTypeEnum
    params: Optional[Dict] = {}

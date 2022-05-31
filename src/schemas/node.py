from pydantic import BaseModel
from typing import Dict, Optional


class NodeCreateModel(BaseModel):
    title: str
    desk_uuid: str
    type_uuid: str
    params: Optional[Dict] = {}

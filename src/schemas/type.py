from pydantic import BaseModel
from typing import Dict, Optional


class TypeCreateModel(BaseModel):
    title: str
    typology_uuid: str
    params: Optional[Dict] = {}

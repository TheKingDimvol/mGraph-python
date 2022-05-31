from pydantic import BaseModel
from typing import Dict, Optional


class TypologyCreateModel(BaseModel):
    title: str
    params: Optional[Dict] = {}

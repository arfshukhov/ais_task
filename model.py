from typing import List

from pydantic import BaseModel

class Path(BaseModel):
    type: str
    cost: int
    days: int
    path: List
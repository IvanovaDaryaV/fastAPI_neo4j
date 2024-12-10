# pydantic схемы для данных API

from pydantic import BaseModel
from typing import List, Optional

class PersonBase(BaseModel):
    name: str
    age: str

class PersonCreate(PersonBase):
    pass

class PersonResponse(PersonBase):
    id: str

class RelationshipCreate(BaseModel):
    from_person: str
    to_person: str

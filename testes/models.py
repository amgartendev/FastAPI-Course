from pydantic import BaseModel
from typing import Optional


class Person(BaseModel):
    name: str
    dob: str
    hobbies: Optional[list] = None

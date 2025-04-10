from pydantic import BaseModel
from typing import Optional

class Todo(BaseModel):
    title: str
    description: Optional[str] = None
    done: bool = False

    class Config:
        orm_mode = True

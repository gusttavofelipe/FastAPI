from typing import Optional
from pydantic import BaseModel as SCBasemodel


class CourseSchema(SCBasemodel):
    id: Optional[int]
    title: str
    number_classes: int
    hours: int

    class Config:
        orm_mode = True

from pprint import pprint
from typing import Optional
from pydantic import BaseModel

class Course(BaseModel):
    id: Optional[int] = None
    title: str
    classes: int
    hours: int


courses = [
    Course(id=1, title='Class 1', classes=45, hours=30),
    Course(id=2, title='Class 2', classes=43, hours=50),
    Course(id=3, title='Class 3', classes=42, hours=23),
]
pprint(courses.index(1))
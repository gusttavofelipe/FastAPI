from pprint import pprint
from typing import Optional
from pydantic import BaseModel, validator

class Course(BaseModel):
    id: Optional[int] = None
    title: str
    classes: int
    hours: int

    # VALIDATION
    @validator('title') # campo
    def validate_title(cls, value: str): # value - campo que foi passado no validator
        words = value.split(' ')
        if len(words) < 3:
            raise ValueError('the title must contain at least 3 words')
        return value # sempre retornar value

courses = [
    Course(id=1, title='Class 1 a', classes=45, hours=30),
    Course(id=2, title='Class 2 b', classes=43, hours=50),
    Course(id=3, title='Class 3 c', classes=42, hours=23),
]
pprint(courses)
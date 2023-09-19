from typing import Optional
from pydantic import BaseModel as SCBasemodel, HttpUrl


class ArticleSchema(SCBasemodel):
    id: Optional[int] = None
    title: str
    description: str
    url_font: HttpUrl
    user_id: Optional[int] = None

    class Config:
        orm_mode = True

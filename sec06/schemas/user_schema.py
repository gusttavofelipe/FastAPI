from typing import Optional
from pydantic import BaseModel as SCBasemodel, EmailStr
from schemas.article_schema import ArticleSchema


class UserSchemaBase(SCBasemodel):
    id: Optional[int] = None
    name: str
    lastname: str
    email: EmailStr
    password: str
    is_admin: bool = False

    class Config:
        orm_mode = True


class UserSchemaCreate(UserSchemaBase):
    password: str


class UserSchemaArticles(UserSchemaBase):
    articles: Optional[list[ArticleSchema]]


class UserSchemaUpdate(UserSchemaBase):
    name: Optional[str]
    lastname: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    is_admin: Optional[bool]

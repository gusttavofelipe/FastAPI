from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings


class ArticleModel(settings.DB_Basemodel):
    __tablename__: str = 'articles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    url_font = Column(String(255))
    description = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship(
        'UserModel', back_populates='articles', lazy='joined'
    )

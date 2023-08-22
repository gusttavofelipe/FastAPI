from core.configs import settings
from sqlalchemy import Column, Integer, String


class CourseModel(settings.DBBasemodel): # database table
    __tablename__ = 'courses'

    id: str = Column(Integer, primary_key=True, autoincrement=True)
    title: str = Column(String(255))
    number_classes: str = Column(Integer)
    hours: int = Column(Integer)
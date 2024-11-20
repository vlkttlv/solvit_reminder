from sqlalchemy import Column, Integer, String
from app.database import Base


class Questions(Base):

    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    grade = Column(String)
    technology = Column(String)

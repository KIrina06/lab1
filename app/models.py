from sqlalchemy import Column, Integer, String
from .database import Base

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    address = Column(String, nullable=True)
    work = Column(String, nullable=True)
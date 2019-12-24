from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Todo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    priority = Column(Integer)

    def __str__(self):
        return self.name

    def name_with_priority(self):
        return f"Priority: {self.priority}. Name: {self.name}"

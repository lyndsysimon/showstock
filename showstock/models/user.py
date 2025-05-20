from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    given_name = Column(String, nullable=False)
    family_name = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, given_name='{self.given_name}', family_name='{self.family_name}')>"

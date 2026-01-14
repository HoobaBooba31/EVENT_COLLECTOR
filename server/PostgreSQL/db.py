from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Column, String, Boolean, Integer


Base = declarative_base()


class Permissions(Base):
    
    __tablename__ = "Permissions"

    index = Column(Integer, primary_key=True, unique=True, index=True)
    id = Column(Integer, unique=True)
    if_admin = Column(Boolean, default=False)


class Admins(Base):

    __tablename__ = "Admins"

    index = Column(Integer, primary_key=True, unique=True, index=True)
    id = Column(Integer, unique=True)
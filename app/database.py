from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from sqlalchemy import exc

from config import settings

engine = create_engine(settings.database_url)
session_creator = sessionmaker(engine, expire_on_commit = False)

class Base(DeclarativeBase):
    pass

def create_db():
    Base.metadata.create_all(engine)
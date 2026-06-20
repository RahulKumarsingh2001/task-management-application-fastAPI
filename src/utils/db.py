# config of DB

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.utils.setting import settings

Base = declarative_base()

engine = create_engine(url=settings.DB_CONNECTION_URI)

LocalSession = sessionmaker(bind=engine)


# DB Provider

def get_db():
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()    
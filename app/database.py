from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

from urllib.parse import quote_plus

password = quote_plus(settings.POSTGRES_PASSWORD)  # URL-encode the password for handling special characters

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{settings.POSTGRES_USER}:{password}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#Dependancy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

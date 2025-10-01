from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = "sqlite:///./intelecta.db" # Caminho do SQLite (um arquivo .db local)

# O parâmetro check_same_thread é necessário no SQLite para multithreading
engine = create_engine( SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False}) 

Sessionlocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

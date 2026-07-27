from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config import setting


engine = create_engine(setting.DATABASE_URL)
sessionlocal = sessionmaker(autoflush=False, autocommit = False, bind=engine)

Base = declarative_base()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
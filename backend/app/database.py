from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase,sessionmaker
from .config import settings
class Base(DeclarativeBase): pass
database_url=settings.database_url
if database_url.startswith("postgresql://"):
    database_url=database_url.replace("postgresql://","postgresql+psycopg://",1)
engine=create_engine(database_url,connect_args={"check_same_thread":False} if database_url.startswith("sqlite") else {})
SessionLocal=sessionmaker(bind=engine,autoflush=False,expire_on_commit=False)
def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()

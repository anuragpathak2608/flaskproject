from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models import Base

engine = create_engine('sqlite:///todo.db', convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base.query = db_session.query_property()


def init_db():
    print("Creating db tables")
    Base.metadata.create_all(bind=engine)


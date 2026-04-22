from sqlmodel import SQLModel, create_engine, Session

Database_URL = "sqlite:///sales.db"
engine = create_engine(Database_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
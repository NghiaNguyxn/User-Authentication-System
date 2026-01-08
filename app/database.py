from sqlmodel import Session, SQLModel, create_engine

from .config import settings

engine = create_engine(
    settings.DATABASE_URL,
    # echo=True,           # Log các câu lệnh SQL ra terminal (tiện để debug)
    connect_args={"check_same_thread": False}
)

def create_db_and_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
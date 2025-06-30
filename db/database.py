import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine

load_dotenv()  

SQLITE_DATABASE_NAME = "logs.db"
SQLITE_DATABASE_URL = f"sqlite:///{SQLITE_DATABASE_NAME}"

RENDER_DATABASE_URL = os.getenv("RENDER_DATABASE_URL")

engine = create_engine(RENDER_DATABASE_URL)


# ✅ Dependency to get DB session in routes
def get_session() :
    with Session(engine) as session:
        yield session

# ✅ Function to create tables
def init_db():
    SQLModel.metadata.create_all(bind=engine)
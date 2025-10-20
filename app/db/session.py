from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# SQLite file databse (local)
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# Engine: low-level interface to the DB
# For SQLite we need check_same_thread=False so FastAPI can reuse the connection
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Base class for our ORM models
class Base(DeclarativeBase):
    pass

# Factory that creates DB sessions (one per request)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

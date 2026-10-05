from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

# Default to sqlite for local tests without docker
DEFAULT_DB = "sqlite:///./flowtab.db"
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB)

if "pytest" in sys.modules:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Replace postgresql:// with postgresql+psycopg2://
if SQLALCHEMY_DATABASE_URL.startswith("postgresql://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")

connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

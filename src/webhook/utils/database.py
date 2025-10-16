from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..config import settings

# Create SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL, pool_size=5, max_overflow=10)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for declarative models
Base = declarative_base()

def get_db():
    """
    Generator function to get database session.
    Usage:
        with get_db() as db:
            # use db session here
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
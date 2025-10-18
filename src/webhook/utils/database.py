from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
import logging
import time

from ..config import settings

# Configure database logger
db_logger = logging.getLogger('sqlalchemy.engine')
db_logger.setLevel(logging.INFO)

# Create SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL, pool_size=5, max_overflow=10)

# Add query logging
@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())
    db_logger.debug("Start Query:\n%s\nParameters: %r", statement, parameters)

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop()
    db_logger.info("Query Complete:\n%s\nParameters: %r\nDuration: %.3f seconds", 
                  statement, parameters, total)

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
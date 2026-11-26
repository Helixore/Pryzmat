from contextlib import contextmanager

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker
import json, os


if os.path.exists("config.json"):
    with open("config.json") as f:
        config = json.load(f)
        
    if not config.get("database"):
        raise RuntimeError("Bad database setup.")
else:
    config = os.getenv("config")

config = config.get("database")
url = URL.create("postgresql+psycopg",
          username=config.get("user"),
          password=config.get("password"),
          host=config.get("host"),
          port=config.get("port"),
          database=config.get("database"))

engine = create_engine(url, pool_size=20, max_overflow=15, pool_timeout=15, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
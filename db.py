from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- Config DB ---
DATABASE_URL = "sqlite:///./test.db"  # file SQLite locale

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Map(Base):
    __tablename__ = "map"
    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    data = Column(JSON, index=True)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

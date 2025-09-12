import datetime

from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- Config DB ---
DATABASE_URL = "sqlite:///./test.db"  # file SQLite locale

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)


def post_session(map_id, start_time, final_state, number_of_actions, num_cleaned_tiles, duration, db):
    try:
        session = CleaningSession(map_id=map_id, start_time=start_time, final_state=final_state,
                                  number_of_actions=number_of_actions,
                                  number_of_cleaned_tiles=num_cleaned_tiles, duration=duration)
        db.add(session)
        db.commit()
        db.refresh(session)
    except Exception as e:
        raise e


class CleaningSession(Base):
    __tablename__ = "session"
    id = Column(Integer, primary_key=True, autoincrement=True)
    map_id = Column(Integer)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    final_state = Column(String, nullable=True)  # ad esempio 'success' o 'failure'
    number_of_actions = Column(Integer, default=0)
    number_of_cleaned_tiles = Column(Integer, default=0)
    duration = Column(Integer, nullable=True)  # durata in secondi


class Map(Base):
    __tablename__ = "map"
    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    data = Column(JSON, index=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

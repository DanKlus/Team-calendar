from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///events.db"

Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    start = Column(String, nullable=False)
    backgroundColor = Column(String, nullable=False)
    borderColor = Column(String, nullable=False)
    allDay = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)  # Add name column
    status = Column(String, nullable=False)  # Add status column

def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print("Database initialized and table created.")

if __name__ == '__main__':
    init_db()
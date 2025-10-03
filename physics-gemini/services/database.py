from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

base = declarative_base()

# SQL Response Table
class Response(base):
    __tablename__ = 'responses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String, nullable=False)
    response = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow) 

    def __repr__(self):
        return f"<Response(id={self.id}, question={self.question}, response={self.response}, timestamp={self.timestamp})>"
    
# 3. Database setup (SQLite in this example)
DATABASE_URL = "sqlite:///./responses.db"
engine = create_engine(DATABASE_URL, echo=True, future=True)

# 4. Session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# 5. Create tables if not exist
def init_db():
    base.metadata.create_all(bind=engine)

# 6. Query helper
def get_response_by_id(response_id: int):
    with SessionLocal() as session:
        return session.query(Response).filter(Response.id == response_id).first()

def add_response(question: str, response: str):
    with SessionLocal() as session:
        new_response = Response(question=question, response=response)
        session.add(new_response)
        session.commit()
        session.refresh(new_response)
        return new_response
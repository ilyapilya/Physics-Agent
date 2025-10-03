from sqlalchemy import Column, Integer, String, Datetime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Response(Base):
    __tablename__ = 'responses'

    id = Column(Integer, primary_key=True)
    question = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    timestamp = Column(Datetime, default=datetime.utcnow)


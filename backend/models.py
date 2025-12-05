from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class Ping(Base):
    __tablename__ = "pings"
    id = Column(Integer, primary_key=True)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

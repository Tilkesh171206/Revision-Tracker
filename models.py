from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class RevisionStatus(enum.Enum):
    PENDING = "pending"
    DONE = "done"

class Topic(Base):
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    revisions = relationship("Revision", back_populates="topic", cascade="all, delete-orphan")

class Revision(Base):
    __tablename__ = "revisions"
    
    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    next_revision_date = Column(Date, nullable=False)
    interval_level = Column(Integer, default=0, nullable=False)
    last_interval_days = Column(Float, default=1, nullable=False)
    status = Column(Enum(RevisionStatus), default=RevisionStatus.PENDING, nullable=False)
    
    topic = relationship("Topic", back_populates="revisions")

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class SessionStatus(enum.Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    session_number = Column(Integer, nullable=False)
    name = Column(String, nullable=True)
    
    # Session content
    preparation_notes = Column(Text, nullable=True)
    audio_recording_path = Column(String, nullable=True)
    transcript = Column(Text, nullable=True)
    recap = Column(Text, nullable=True)
    
    # Status
    status = Column(Enum(SessionStatus), default=SessionStatus.PLANNED)
    
    # Schedule
    scheduled_date = Column(DateTime, nullable=True)
    actual_date = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    campaign = relationship("Campaign", back_populates="sessions")
    npcs = relationship("NPC", back_populates="session")
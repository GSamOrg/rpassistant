from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class NPC(Base):
    __tablename__ = "npcs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    
    # Basic info
    name = Column(String, nullable=False)
    role = Column(String, nullable=True)  # shopkeeper, witness, antagonist, etc.
    
    # Description
    appearance = Column(Text, nullable=True)
    personality_traits = Column(Text, nullable=True)
    backstory = Column(Text, nullable=True)
    
    # Game mechanics
    relevant_skills_stats = Column(Text, nullable=True)  # JSON or text
    relationship_to_campaign = Column(Text, nullable=True)
    
    # Generation info
    generated_parameters = Column(Text, nullable=True)  # JSON of original parameters
    ai_generated = Column(Boolean, default=True)
    
    # Integration status
    integration_status = Column(String, default="pending")  # pending, approved, integrated
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    session = relationship("Session", back_populates="npcs")
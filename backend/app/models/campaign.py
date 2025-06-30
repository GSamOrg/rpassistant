from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    rpg_system = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    
    # Owner
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Campaign content
    campaign_notes = Column(Text, nullable=True)
    uploaded_documents = Column(Text, nullable=True)  # JSON array of file paths
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="campaigns")
    sessions = relationship("Session", back_populates="campaign")
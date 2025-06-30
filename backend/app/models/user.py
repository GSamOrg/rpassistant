from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # OAuth fields
    google_id = Column(String, unique=True, nullable=True)
    discord_id = Column(String, unique=True, nullable=True)
    
    # Profile info
    full_name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    
    # Subscription
    subscription_status = Column(String, default="free")
    subscription_expires = Column(DateTime, nullable=True)
    
    # Discord integration settings
    discord_integration_settings = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    campaigns = relationship("Campaign", back_populates="owner")
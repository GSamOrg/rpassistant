from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..database import get_db
from ..models.session import Session as SessionModel, SessionStatus
from ..models.campaign import Campaign
from ..models.user import User
from ..routers.auth import get_current_user
from pydantic import BaseModel

router = APIRouter()

class SessionCreate(BaseModel):
    campaign_id: int
    session_number: int
    name: str = None
    scheduled_date: Optional[datetime] = None

class SessionUpdate(BaseModel):
    name: str = None
    preparation_notes: str = None
    status: SessionStatus = None
    scheduled_date: Optional[datetime] = None
    actual_date: Optional[datetime] = None
    recap: str = None

class SessionResponse(BaseModel):
    id: int
    campaign_id: int
    session_number: int
    name: str = None
    preparation_notes: str = None
    status: SessionStatus
    scheduled_date: Optional[datetime] = None
    actual_date: Optional[datetime] = None
    recap: str = None
    created_at: str

    class Config:
        from_attributes = True

async def verify_campaign_access(campaign_id: int, current_user: User, db: Session):
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.owner_id == current_user.id
    ).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.post("/", response_model=SessionResponse)
async def create_session(
    session: SessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await verify_campaign_access(session.campaign_id, current_user, db)
    
    db_session = SessionModel(
        campaign_id=session.campaign_id,
        session_number=session.session_number,
        name=session.name,
        scheduled_date=session.scheduled_date
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/campaign/{campaign_id}", response_model=List[SessionResponse])
async def list_sessions(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await verify_campaign_access(campaign_id, current_user, db)
    
    sessions = db.query(SessionModel).filter(
        SessionModel.campaign_id == campaign_id
    ).order_by(SessionModel.session_number).all()
    return sessions

@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(SessionModel).join(Campaign).filter(
        SessionModel.id == session_id,
        Campaign.owner_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.put("/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: int,
    session_update: SessionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(SessionModel).join(Campaign).filter(
        SessionModel.id == session_id,
        Campaign.owner_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    for field, value in session_update.model_dump(exclude_unset=True).items():
        setattr(session, field, value)
    
    db.commit()
    db.refresh(session)
    return session

@router.delete("/{session_id}")
async def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(SessionModel).join(Campaign).filter(
        SessionModel.id == session_id,
        Campaign.owner_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db.delete(session)
    db.commit()
    return {"message": "Session deleted successfully"}
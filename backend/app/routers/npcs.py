from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.npc import NPC
from ..models.session import Session as SessionModel
from ..models.campaign import Campaign
from ..models.user import User
from ..routers.auth import get_current_user
from pydantic import BaseModel

router = APIRouter()

class NPCCreate(BaseModel):
    session_id: int
    name: str
    role: str = None
    appearance: str = None
    personality_traits: str = None
    backstory: str = None
    relevant_skills_stats: str = None
    relationship_to_campaign: str = None
    generated_parameters: str = None

class NPCUpdate(BaseModel):
    name: str = None
    role: str = None
    appearance: str = None
    personality_traits: str = None
    backstory: str = None
    relevant_skills_stats: str = None
    relationship_to_campaign: str = None
    integration_status: str = None

class NPCResponse(BaseModel):
    id: int
    session_id: int
    name: str
    role: str = None
    appearance: str = None
    personality_traits: str = None
    backstory: str = None
    relevant_skills_stats: str = None
    relationship_to_campaign: str = None
    integration_status: str
    ai_generated: bool
    created_at: str

    class Config:
        from_attributes = True

async def verify_session_access(session_id: int, current_user: User, db: Session):
    session = db.query(SessionModel).join(Campaign).filter(
        SessionModel.id == session_id,
        Campaign.owner_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.post("/", response_model=NPCResponse)
async def create_npc(
    npc: NPCCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await verify_session_access(npc.session_id, current_user, db)
    
    db_npc = NPC(
        session_id=npc.session_id,
        name=npc.name,
        role=npc.role,
        appearance=npc.appearance,
        personality_traits=npc.personality_traits,
        backstory=npc.backstory,
        relevant_skills_stats=npc.relevant_skills_stats,
        relationship_to_campaign=npc.relationship_to_campaign,
        generated_parameters=npc.generated_parameters
    )
    db.add(db_npc)
    db.commit()
    db.refresh(db_npc)
    return db_npc

@router.get("/session/{session_id}", response_model=List[NPCResponse])
async def list_npcs(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await verify_session_access(session_id, current_user, db)
    
    npcs = db.query(NPC).filter(NPC.session_id == session_id).all()
    return npcs

@router.get("/{npc_id}", response_model=NPCResponse)
async def get_npc(
    npc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    npc = db.query(NPC).join(SessionModel).join(Campaign).filter(
        NPC.id == npc_id,
        Campaign.owner_id == current_user.id
    ).first()
    if not npc:
        raise HTTPException(status_code=404, detail="NPC not found")
    return npc

@router.put("/{npc_id}", response_model=NPCResponse)
async def update_npc(
    npc_id: int,
    npc_update: NPCUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    npc = db.query(NPC).join(SessionModel).join(Campaign).filter(
        NPC.id == npc_id,
        Campaign.owner_id == current_user.id
    ).first()
    if not npc:
        raise HTTPException(status_code=404, detail="NPC not found")
    
    for field, value in npc_update.model_dump(exclude_unset=True).items():
        setattr(npc, field, value)
    
    db.commit()
    db.refresh(npc)
    return npc

@router.delete("/{npc_id}")
async def delete_npc(
    npc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    npc = db.query(NPC).join(SessionModel).join(Campaign).filter(
        NPC.id == npc_id,
        Campaign.owner_id == current_user.id
    ).first()
    if not npc:
        raise HTTPException(status_code=404, detail="NPC not found")
    
    db.delete(npc)
    db.commit()
    return {"message": "NPC deleted successfully"}
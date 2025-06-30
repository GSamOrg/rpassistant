from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.campaign import Campaign
from ..models.user import User
from ..routers.auth import get_current_user
from pydantic import BaseModel

router = APIRouter()

class CampaignCreate(BaseModel):
    name: str
    rpg_system: str
    description: str = None

class CampaignUpdate(BaseModel):
    name: str = None
    rpg_system: str = None
    description: str = None
    campaign_notes: str = None

class CampaignResponse(BaseModel):
    id: int
    name: str
    rpg_system: str
    description: str = None
    campaign_notes: str = None
    created_at: str
    updated_at: str = None

    class Config:
        from_attributes = True

@router.post("/", response_model=CampaignResponse)
async def create_campaign(
    campaign: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_campaign = Campaign(
        name=campaign.name,
        rpg_system=campaign.rpg_system,
        description=campaign.description,
        owner_id=current_user.id
    )
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign

@router.get("/", response_model=List[CampaignResponse])
async def list_campaigns(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    campaigns = db.query(Campaign).filter(Campaign.owner_id == current_user.id).all()
    return campaigns

@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.owner_id == current_user.id
    ).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.put("/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(
    campaign_id: int,
    campaign_update: CampaignUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.owner_id == current_user.id
    ).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    for field, value in campaign_update.model_dump(exclude_unset=True).items():
        setattr(campaign, field, value)
    
    db.commit()
    db.refresh(campaign)
    return campaign

@router.delete("/{campaign_id}")
async def delete_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.owner_id == current_user.id
    ).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    db.delete(campaign)
    db.commit()
    return {"message": "Campaign deleted successfully"}
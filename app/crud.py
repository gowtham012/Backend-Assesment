from sqlalchemy.orm import Session
from app import models, schemas

def create_lead(db: Session, lead_in: schemas.LeadCreate):
    db_lead = models.Lead(
        first_name=lead_in.first_name,
        last_name=lead_in.last_name,
        email=lead_in.email,
        resume=lead_in.resume
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

def get_leads(db: Session):
    return db.query(models.Lead).all()

def get_lead(db: Session, lead_id: int):
    return db.query(models.Lead).filter(models.Lead.id == lead_id).first()

def update_lead_state(db: Session, lead: models.Lead, lead_update: schemas.LeadUpdate):
    lead.state = lead_update.state
    db.commit()
    db.refresh(lead)
    return lead

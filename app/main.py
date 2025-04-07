from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, crud, email_utils, auth
from app.database import engine, SessionLocal

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lead Management Service")


# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/leads", response_model=schemas.LeadOut, status_code=201)
def create_lead(
    lead_in: schemas.LeadCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Create a lead with initial state 'PENDING'
    lead = crud.create_lead(db, lead_in)
    # Trigger background email notifications
    background_tasks.add_task(email_utils.send_notification_emails, lead)
    return lead



@app.get("/leads", response_model=list[schemas.LeadOut])
def list_leads(
    db: Session = Depends(get_db),
    user: str = Depends(auth.get_current_user)
):
    return crud.get_leads(db)


@app.put("/leads/{lead_id}", response_model=schemas.LeadOut)
def update_lead_state(
    lead_id: int,
    lead_update: schemas.LeadUpdate,
    db: Session = Depends(get_db),
    user: str = Depends(auth.get_current_user)
):
    lead = crud.get_lead(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    updated_lead = crud.update_lead_state(db, lead, lead_update)
    return updated_lead

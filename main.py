from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import date, timedelta
from typing import Tuple

from database import get_db, init_db
from models import Topic, Revision, RevisionStatus

app = FastAPI(title="NEET Spaced Repetition Tracker")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

BASE_INTERVALS = [1, 3, 7, 14, 21, 30, 60]

@app.on_event("startup")
async def startup_event():
    try:
        init_db()
    except Exception as e:
        print(f"Database initialization failed: {e}")

def calculate_next_interval(difficulty: str, interval_level: int, last_interval_days: float) -> Tuple[int, float]:
    """
    Calculate next revision interval based on difficulty and current level.
    Returns (new_interval_level, new_interval_days)
    """
    if difficulty == "hard":
        return 0, 1.0
    
    if difficulty == "easy":
        if interval_level < len(BASE_INTERVALS):
            return interval_level + 1, float(BASE_INTERVALS[interval_level])
        else:
            return interval_level, last_interval_days * 2.5
    
    if difficulty == "medium":
        if interval_level < len(BASE_INTERVALS):
            return interval_level + 1, float(BASE_INTERVALS[interval_level])
        else:
            return interval_level, last_interval_days * 1.5
    
    return interval_level, last_interval_days

@app.get("/")
async def dashboard(request: Request, db: Session = Depends(get_db)):
    try:
        today = date.today()
        
        today_revisions = db.query(Revision).join(Topic).filter(
            Revision.next_revision_date == today,
            Revision.status == RevisionStatus.PENDING
        ).order_by(Revision.next_revision_date).all()
        
        upcoming_revisions = db.query(Revision).join(Topic).filter(
            Revision.next_revision_date > today,
            Revision.status == RevisionStatus.PENDING
        ).order_by(Revision.next_revision_date).limit(10).all()
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "today_revisions": today_revisions,
            "upcoming_revisions": upcoming_revisions,
            "today": today
        })
    except SQLAlchemyError as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Database error occurred",
            "today_revisions": [],
            "upcoming_revisions": [],
            "today": date.today()
        })

@app.post("/add")
async def add_topic(request: Request, topic_name: str = Form(...), db: Session = Depends(get_db)):
    try:
        if not topic_name.strip():
            return RedirectResponse(url="/?error=Topic name cannot be empty", status_code=303)
        
        existing_topic = db.query(Topic).filter(Topic.name == topic_name.strip()).first()
        if existing_topic:
            return RedirectResponse(url="/?error=Topic already exists", status_code=303)
        
        topic = Topic(name=topic_name.strip())
        db.add(topic)
        db.flush()
        
        revision = Revision(
            topic_id=topic.id,
            next_revision_date=date.today() + timedelta(days=1),
            interval_level=0,
            last_interval_days=1.0,
            status=RevisionStatus.PENDING
        )
        db.add(revision)
        db.commit()
        
        return RedirectResponse(url="/", status_code=303)
    except SQLAlchemyError:
        db.rollback()
        return RedirectResponse(url="/?error=Failed to add topic", status_code=303)

@app.post("/review/{revision_id}")
async def review_revision(
    request: Request, 
    revision_id: int, 
    difficulty: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        if difficulty not in ["easy", "medium", "hard"]:
            raise HTTPException(status_code=400, detail="Invalid difficulty level")
        
        revision = db.query(Revision).filter(Revision.id == revision_id).first()
        if not revision:
            raise HTTPException(status_code=404, detail="Revision not found")
        
        new_level, new_interval = calculate_next_interval(
            difficulty, revision.interval_level, revision.last_interval_days
        )
        
        revision.interval_level = new_level
        revision.last_interval_days = new_interval
        revision.next_revision_date = date.today() + timedelta(days=int(new_interval))
        revision.status = RevisionStatus.PENDING
        
        db.commit()
        
        return RedirectResponse(url="/", status_code=303)
    except HTTPException:
        raise
    except SQLAlchemyError:
        db.rollback()
        return RedirectResponse(url="/?error=Failed to update revision", status_code=303)

@app.post("/delete/{topic_id}")
async def delete_topic(request: Request, topic_id: int, db: Session = Depends(get_db)):
    try:
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            raise HTTPException(status_code=404, detail="Topic not found")
        
        db.delete(topic)
        db.commit()
        
        return RedirectResponse(url="/", status_code=303)
    except HTTPException:
        raise
    except SQLAlchemyError:
        db.rollback()
        return RedirectResponse(url="/?error=Failed to delete topic", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database_test import SessionLocal, Base, engine
from sqlalchemy import text

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1;"))
    return {"PostgreSQL test": result.scalar()}

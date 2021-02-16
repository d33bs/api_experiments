from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import database_ops
import pydantic_models
import sqlalchemy_models

from database import SessionLocal, engine

sqlalchemy_models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/wine/", response_model=List[pydantic_models.WineRecord])
def get_wine(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return database_ops.get_wine_records(db, skip=skip, limit=limit)

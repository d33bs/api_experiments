from sqlalchemy.orm import Session

import pydantic_models
import sqlalchemy_models


def get_wine_records(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(sqlalchemy_models.Wine).offset(skip).limit(limit).all()


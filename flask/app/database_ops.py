from typing import List
from sqlalchemy.orm import Session

import sqlalchemy_models


def get_wine_records(db_session: Session, skip: int = 0, limit: int = 1000):
    return db_session.query(sqlalchemy_models.Wine).offset(skip).limit(limit).all()

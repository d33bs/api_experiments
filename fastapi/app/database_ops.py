from typing import List
from sqlalchemy.orm import Session

import pydantic_models
import sqlalchemy_models


def get_wine_records(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(sqlalchemy_models.Wine).offset(skip).limit(limit).all()


def post_wine_records(db: Session, wine_records: List[pydantic_models.WineRecord]):
    new_wine_records = [
        sqlalchemy_models.Wine(**record.dict()) for record in wine_records
    ]
    db.add_all(new_wine_records)
    db.commit()
    records_processed = pydantic_models.WineRecordsProcessed(
        processed=len(new_wine_records)
    )
    return records_processed

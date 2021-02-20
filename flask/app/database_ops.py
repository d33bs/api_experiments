from typing import List

from sqlalchemy.orm import Session

import marshmallow_schemas
import sqlalchemy_models


def get_wine_records(db_session: Session, skip: int = 0, limit: int = 1000):
    print(limit)
    return db_session.query(sqlalchemy_models.Wine).offset(skip).limit(limit).all()


def post_wine_records(db_session: Session, wine_records: list):
    new_wine_records = [sqlalchemy_models.Wine(**record) for record in wine_records]
    db_session.add_all(new_wine_records)
    db_session.commit()
    records_processed = marshmallow_schemas.WineRecordsProcessed().load(
        {"processed": len(new_wine_records)}
    )
    return records_processed

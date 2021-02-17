from typing import List, Optional

import pandas as pd
from fastapi import Depends, FastAPI, HTTPException
from sklearn import datasets
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


@app.get("/sklearn_wine/", response_model=List[pydantic_models.WineRecord])
def get_sklearn_wine():
    # load wine dataset from sklearn
    wine = datasets.load_wine()

    # load wine dataset as pandas dataframe
    df = pd.DataFrame(wine.data, columns=wine.feature_names)

    # replace '/' char in column name with '_'
    df.columns = [col.replace("/", "_") for col in df.columns]

    # set id col to index number
    df["id"] = df.index

    # export data as record-orientated dict
    df_dict = df.to_dict(orient="records")

    # convert dict to list of Wine model records
    result = [sqlalchemy_models.Wine(**record) for record in df_dict]

    return result


@app.get("/sqlite_wine/", response_model=List[pydantic_models.WineRecord])
def get_wine(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return database_ops.get_wine_records(db, skip=skip, limit=limit)


@app.post("/sqlite_wine/", response_model=pydantic_models.WineRecordsProcessed)
def post_wine(
    wine_records: List[pydantic_models.WineRecord], db: Session = Depends(get_db)
):
    return database_ops.post_wine_records(db=db, wine_records=wine_records)

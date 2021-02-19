from typing import List, Optional

import pandas as pd
from flask import Flask, request, jsonify
from sklearn import datasets
from sqlalchemy.orm import Session

import database_ops
import marshmallow_schemas
import sqlalchemy_models
from database import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def read_root():
    return {"Hello": "World"}


@app.route("/items/<int:item_id>", methods=["GET"])
def read_item(item_id: int, q: Optional[str] = None):
    q = request.args.get("q")

    return {"item_id": item_id, "q": q}



@app.route("/sklearn_wine", methods=["GET"])
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

    return jsonify(df_dict)


@app.route("/sqlite_wine", methods=["GET"])
def get_wine(skip: int = 0, limit: int = 100, db_session: Session = db.session):
    return database_ops.get_wine_records(db_session=db_session, skip=skip, limit=limit)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")

import json
from typing import List, Optional

import pandas as pd
from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from sklearn import datasets
from sqlalchemy.orm import Session
from werkzeug.exceptions import HTTPException

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

ma = Marshmallow(app)

wine = marshmallow_schemas.Wine()
wines = marshmallow_schemas.Wine(many=True)


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
    df["uid"] = df.index

    # export data as record-orientated dict
    df_dict = df.to_dict(orient="records")

    # convert dict to list of Wine model records
    result = [sqlalchemy_models.Wine(**record) for record in df_dict]

    return jsonify(wines.dump(result))


@app.route("/sqlite_wine", methods=["GET"])
def get_wine(db_session: Session = db.session):
    skip = request.args.get("skip")
    limit = request.args.get("limit")
    return jsonify(
        wines.dump(
            database_ops.get_wine_records(db_session=db_session, skip=skip, limit=limit)
        )
    )


@app.route("/sqlite_wine", methods=["POST"])
def post_wine(db_session: Session = db.session):
    wine_records = json.loads(request.data)
    return database_ops.post_wine_records(
        db_session=db_session, wine_records=wine_records
    )


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {"code": e.code, "name": e.name, "description": e.description,}
    )
    response.content_type = "application/json"
    return response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")

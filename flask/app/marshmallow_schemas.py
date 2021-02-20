from typing import List, Optional

import marshmallow as ma
from marshmallow_sqlalchemy import ModelSchema, SQLAlchemyAutoSchema

from sqlalchemy_models import Wine


class Wine(SQLAlchemyAutoSchema):
    class Meta:
        model = Wine


class WineRecordsProcessed(ma.Schema):
    class Meta:
        fields = ("processed", "message")

    processed = ma.fields.Int()
    message = ma.fields.Str()

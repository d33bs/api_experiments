from typing import List, Optional

from marshmallow_sqlalchemy import ModelSchema


class Wine(ModelSchema):
    class Meta:
        fields = (
            "uid",
            "alcohol",
            "malic_acid",
            "ash",
            "alcalinity_of_ash",
            "magnesium",
            "total_phenols",
            "flavanoids",
            "nonflavanoid_phenols",
            "proanthocyanins",
            "color_intensity",
            "hue",
            "od280_od315_of_diluted_wines",
            "proline",
        )


class WineRecordsProcessed(ModelSchema):
    class Meta:
        fields = ("processed", "message")

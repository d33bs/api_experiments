from typing import List, Optional

from pydantic import BaseModel


class WineRecord(BaseModel):
    uid: int
    alcohol: float
    malic_acid: float
    ash: float
    alcalinity_of_ash: float
    magnesium: float
    total_phenols: float
    flavanoids: float
    nonflavanoid_phenols: float
    proanthocyanins: float
    color_intensity: float
    hue: float
    od280_od315_of_diluted_wines: float
    proline: float

    class Config:
        orm_mode = True


class WineRecordsProcessed(BaseModel):
    processed: int
    message: Optional[str] = None

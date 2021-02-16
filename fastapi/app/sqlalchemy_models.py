from sqlalchemy import Column, Integer, Float
from database import Base


class Wine(Base):
    __tablename__ = "wine"

    id = Column(Integer, primary_key=True)  # auto-increment should be default
    alcohol = Column(Float, default=0.0)
    malic_acid = Column(Float, default=0.0)
    ash = Column(Float, default=0.0)
    alcalinity_of_ash = Column(Float, default=0.0)
    magnesium = Column(Float, default=0.0)
    total_phenols = Column(Float, default=0.0)
    flavanoids = Column(Float, default=0.0)
    nonflavanoid_phenols = Column(Float, default=0.0)
    proanthocyanins = Column(Float, default=0.0)
    color_intensity = Column(Float, default=0.0)
    hue = Column(Float, default=0.0)
    od280_od315_of_diluted_wines = Column(Float, default=0.0)
    proline = Column(Float, default=0.0)


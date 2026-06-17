from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    iso_code = Column(String(3), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    region = Column(String(100))
    sub_region = Column(String(100))
    income_level = Column(String(100))

    data_points = relationship("DataPoint", back_populates="country")

class Indicator(Base):
    __tablename__ = "indicators"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    unit = Column(String(50))
    description = Column(Text)

    data_points = relationship("DataPoint", back_populates="indicator")

class DataPoint(Base):
    __tablename__ = "data_points"

    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey("countries.id", ondelete="CASCADE"), nullable=False)
    indicator_id = Column(Integer, ForeignKey("indicators.id", ondelete="CASCADE"), nullable=False)
    year = Column(Integer, nullable=False, index=True)
    value = Column(Numeric, nullable=False)

    country = relationship("Country", back_populates="data_points")
    indicator = relationship("Indicator", back_populates="data_points")

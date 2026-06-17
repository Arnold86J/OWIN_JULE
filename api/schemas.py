from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal

class IndicatorBase(BaseModel):
    code: str
    name: str
    unit: Optional[str] = None
    description: Optional[str] = None

class Indicator(IndicatorBase):
    id: int

    class Config:
        from_attributes = True

class DataPointBase(BaseModel):
    year: int
    value: Decimal

class DataPoint(DataPointBase):
    pass

    class Config:
        from_attributes = True

class IndicatorData(BaseModel):
    indicator_code: str
    country_iso: str
    data: List[DataPoint]

class AnalysisPrompt(BaseModel):
    system_prompt: str
    user_prompt: str

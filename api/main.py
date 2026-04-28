from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from fastapi_pagination import LimitOffsetPage, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

from . import models, schemas, database

app = FastAPI(title="World Data Insight API")

@app.get("/search", response_model=LimitOffsetPage[schemas.Indicator])
def search_indicators(
    q: str = Query(..., description="Search query for indicator name or code"),
    db: Session = Depends(database.get_db)
):
    """Search for indicators by name or code (slug)."""
    search_filter = or_(
        models.Indicator.name.ilike(f"%{q}%"),
        models.Indicator.code.ilike(f"%{q}%")
    )
    query = db.query(models.Indicator).filter(search_filter)
    return paginate(query)

@app.get("/data/{indicator_code}", response_model=schemas.IndicatorData)
def get_indicator_data(
    indicator_code: str,
    iso_code: str = Query(..., description="Country ISO alpha-3 code"),
    start_year: Optional[int] = None,
    end_year: Optional[int] = None,
    db: Session = Depends(database.get_db)
):
    """Retrieve data points for a specific indicator and country, with optional year range."""
    # 1. Verify Indicator
    indicator = db.query(models.Indicator).filter(models.Indicator.code == indicator_code).first()
    if not indicator:
        raise HTTPException(status_code=404, detail="Indicator not found")

    # 2. Verify Country
    country = db.query(models.Country).filter(models.Country.iso_code == iso_code).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    # 3. Query Data Points
    query = db.query(models.DataPoint).filter(
        models.DataPoint.indicator_id == indicator.id,
        models.DataPoint.country_id == country.id
    )

    if start_year is not None:
        query = query.filter(models.DataPoint.year >= start_year)
    if end_year is not None:
        query = query.filter(models.DataPoint.year <= end_year)

    data_points = query.order_by(models.DataPoint.year).all()

    return {
        "indicator_code": indicator_code,
        "country_iso": iso_code,
        "data": data_points
    }

add_pagination(app)

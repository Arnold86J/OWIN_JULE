from fastapi import FastAPI, Depends, HTTPException, Query, Request, Response
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from fastapi_pagination import LimitOffsetPage, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

from . import models, schemas, database, cache as cache_utils, analytics
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

def key_builder(
    func,
    namespace: Optional[str] = "",
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
):
    from fastapi_cache import FastAPICache
    prefix = FastAPICache.get_prefix()
    cache_key = f"{prefix}:{namespace}:{func.__module__}:{func.__name__}:{args}:{kwargs}"
    # Filter out common objects like 'db' or 'request' that shouldn't be part of the key
    filtered_kwargs = {k: v for k, v in kwargs.items() if k not in ["db", "request", "response"]}
    return f"{prefix}:{namespace}:{func.__module__}:{func.__name__}:{args}:{filtered_kwargs}"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize cache only once with all parameters
    await cache_utils.init_cache(key_builder=key_builder)
    yield

app = FastAPI(title="World Data Insight API", lifespan=lifespan)

@app.get("/search", response_model=LimitOffsetPage[schemas.Indicator])
@cache(expire=86400)
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
@cache(expire=86400)
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

@app.get("/data/{indicator_code}/analysis-prompt", response_model=schemas.AnalysisPrompt)
@cache(expire=86400)
def get_analysis_prompt(
    indicator_code: str,
    iso_code: str = Query(..., description="Country ISO alpha-3 code"),
    start_year: Optional[int] = None,
    end_year: Optional[int] = None,
    db: Session = Depends(database.get_db)
):
    """Generates an LLM prompt for analyzing data trends."""
    # 1. Fetch data (Reuse logic or call internal helper if refactored)
    indicator = db.query(models.Indicator).filter(models.Indicator.code == indicator_code).first()
    if not indicator:
        raise HTTPException(status_code=404, detail="Indicator not found")

    country = db.query(models.Country).filter(models.Country.iso_code == iso_code).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    query = db.query(models.DataPoint).filter(
        models.DataPoint.indicator_id == indicator.id,
        models.DataPoint.country_id == country.id
    )
    if start_year is not None:
        query = query.filter(models.DataPoint.year >= start_year)
    if end_year is not None:
        query = query.filter(models.DataPoint.year <= end_year)

    data_points = query.order_by(models.DataPoint.year).all()

    # Convert ORM objects to dicts for analytics module
    data_dicts = [{"year": dp.year, "value": dp.value} for dp in data_points]

    return analytics.generate_ai_analysis_prompt(
        indicator_name=indicator.name,
        unit=indicator.unit or "unité",
        location=country.full_name,
        data_points=data_dicts
    )

add_pagination(app)

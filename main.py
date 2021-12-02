from typing import List

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn

# import core.crud as crud
from core.calcs.scholes import scholes

import core.models.models as models
import core.schemas.schemas as schemas

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

@app.get("/")
async def root():
    return {'message': 'Hello World!'}

@app.get("/underlyings", response_model=models.Underlying)
async def get_underlyings():
    return schemas.UnderlyingSchema.get_all()

@app.get("/maturities", response_model=models.Maturity)
async def get_maturities():
    return schemas.MaturitySchema.get_all()

# @app.get("/details", response_model=models.ProductDetails)
# async def get_product_details():
#     return schemas.ProductDetails.get_all()

@app.post("/quote", response_model=models.Quote_Out)
async def quote(inputs: models.Quote_In):
    return scholes(inputs)

@app.get("/quotes", response_model=List[models.Quote])
async def filter_quotes(filter_field: str = "", filter_value: str = ""):
    quotes = schemas.QuoteSchema.filter(filter_field, filter_value)
    return quotes

@app.post("/save_quote")
async def save_quote(quote: models.Quote):
    schemas.QuoteSchema.store(quote)

@app.post("/portfolio", response_model=List[models.PortfolioItem])
async def portfolio():
    pass

# @app.get("/vol_curve")
# async def vol_curve(t: date, underlying: str, maturity: date, type: str, source: str = "LME"):
#     return schemas.VolCurve.get(underlying, maturity, type, t, source)
# 

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

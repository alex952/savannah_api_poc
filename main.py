from typing import List

from datetime import date, datetime

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn

# import core.crud as crud
# from core.calcs.scholes import scholes

import core.models.models as models
# import core.schemas.schemas as schemas

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

@app.get("/underlyings", response_model=List[models.Underlying])
async def get_underlyings():
    return [models.Underlying(name='LAD')]
    # return schemas.UnderlyingSchema.get_all()

@app.get("/maturities", response_model=List[models.Maturity])
async def get_maturities():
    return [models.Maturity(name='X1')]
    # return schemas.MaturitySchema.get_all()

@app.get("/details", response_model=models.ProductDetails)
async def get_product_details(product: models.Product):
    return models.ProductDetails(product=product,
            expiry=date.today(),
            prompt=date.today(),
            basis=1334.3,
            forward_price=1335,
            interest=1.2,
            vol=13.3,
            div=0.3)
    # return schemas.ProductDetails.get_all()

@app.post("/quote", response_model=models.QuoteLine_OUT)
async def quote(inputs: models.QuoteLine_IN):
    return models.QuoteLine_OUT(price=12.3, vol=33.4)
    # return scholes(inputs)

@app.get("/quotes", response_model=List[models.Quote])
async def filter_quotes(filter_field: str = "", filter_value: str = ""):
    return [models.Quote(quote_lines=[models.QuoteStructureLine(quote_in=models.QuoteLine_IN(),
                                                                quote_out=models.QuoteLine_OUT())],
                         product=models.Product(underlying='LAD', maturity='X1'),
                         strategy='Butterfly',
                         counterparty='Test',
                         created_by='alex',
                         created_at=datetime.now())]
    # quotes = schemas.QuoteSchema.filter(filter_field, filter_value)
    # return quotes

@app.post("/save_quote")
async def save_quote(quote: models.Quote):
    # schemas.QuoteSchema.store(quote)
    return

@app.post("/portfolio", response_model=List[models.PortfolioItem])
async def portfolio():
    return [models.PortfolioItem(product=models.Product(name="LAD", maturity="X1"),
                                 greeks=models.Greeks(delta=1.2,
                                                      gamma=1.3,
                                                      theta=1.3,
                                                      vega=3.3,
                                                      rho=4.4))]

# @app.get("/vol_curve")
# async def vol_curve(t: date, underlying: str, maturity: date, type: str, source: str = "LME"):
#     return schemas.VolCurve.get(underlying, maturity, type, t, source)
# 

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

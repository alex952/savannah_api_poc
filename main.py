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

import logging as logger

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


@app.post("/quote", response_model=models.Quote_Out)
async def quote(inputs: models.Quote_In):
    return scholes(inputs)

@app.get("/quotes", response_model=List[models.Quote])
async def saved_quotes():
    quotes = schemas.QuoteSchema.get_all()
    print(quotes)
    print(quotes[0])
    print(quotes[0].quote_lines)
    print(len(quotes[0].quote_lines))
    print(dict(quotes[0].quote_lines[0].__dict__))
    return quotes


@app.post("/save_quote")
async def save_quote(quote: models.Quote):
    schemas.QuoteSchema.store(created_by='alex', quote_lines=[q.dict() for q in quote.quote_lines])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

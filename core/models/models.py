from __future__ import annotations
from enum import Enum
from typing import Optional, List
from datetime import datetime, date

from pydantic import BaseModel

class CallOrPutEnum(str, Enum):
    Call = 'Call'
    Put = 'Put'

class Underlying(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Maturity(BaseModel):
    name: str

    expiry: date
    prompt: date

    class Config:
        orm_mode = True


class Product:
    underlying: Underlying
    maturity: Maturity

    class Config:
        orm_mode = True


class ProductDetails:
    product: Product

    basis: float
    forward_price: float
    interest: float
    vol: float
    div: float


class Quote_In(BaseModel):
    product: Product
    call_or_put: CallOrPutEnum
    strike_price: float

    class Config:
        orm_mode = True


class Quote_Out(BaseModel):
    price: float
    vol: Optional[float]

    greeks: Optional[Greeks]


class Greeks(BaseModel):
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float


class Quote(BaseModel):
    quote_lines: List[Quote_In]

    product: Product
    strategy: str
    counterparty: str
    created_by: str
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class PortfolioItem(BaseModel):
    underlying: Underlying
    greeks: Greeks


# class VolCurvePoint_IN(BaseModel):
#     product: Product
#     vol_curve_date: date
#     vol_curve_source: str
#     vol_type: str


# class VolCurvePoint(VolCurvePoint_IN):
#     value


from __future__ import annotations
from enum import Enum
from typing import Optional, List
from datetime import datetime, date

from pydantic import BaseModel

class SideEnum(str, Enum):
    Call = 'Call'
    Put = 'Put'

class Underlying(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Maturity(BaseModel):
    name: str

    class Config:
        orm_mode = True


# class Product:
#     underlying: Underlying
#     maturity: Maturity
# 
#     class Config:
#         orm_mode = True


class Quote_In(BaseModel):
    side: SideEnum
    basis: float
    strike_price: float
    vol: float
    interest: float
    dividend: float
    maturity: date

    class Config:
        orm_mode = True


class Quote_Out(BaseModel):
    price: float
    delta: Optional[float]
    gamma: Optional[float]
    theta: Optional[float]
    vega: Optional[float]
    rho: Optional[float]


class Quote(BaseModel):
    quote_lines: List[Quote_In]

    product: Product
    strategy: str
    counterparty: str
    created_by: str
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

class VolCurvePoint_IN(BaseModel):
    product: Product
    vol_curve_date: date
    vol_curve_source: str
    vol_type: str


# class VolCurvePoint(VolCurvePoint_IN):
#     value


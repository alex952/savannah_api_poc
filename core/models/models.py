from __future__ import annotations
from enum import Enum
from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel

class SideEnum(str, Enum):
    Call = 'Call'
    Put = 'Put'

class Quote_In(BaseModel):
    side: SideEnum
    spot_px: float
    strike_price: float
    vol: float
    interest: float
    dividend: float
    t: float

    class Config:
        orm_mode = True

class Quote_Out(BaseModel):
    price: float
    delta: Optional[float]
    gamma: Optional[float]
    theta: Optional[float]
    vega: Optional[float]
    rho: Optional[float]

    class Config:
        orm_mode = True
from __future__ import print_function

import numpy as np

from core.models.models import Quote_In, Quote_Out, SideEnum


def cnd(d):
    A1 = 0.31938153
    A2 = -0.356563782
    A3 = 1.781477937
    A4 = -1.821255978
    A5 = 1.330274429
    RSQRT2PI = 0.39894228040143267793994605993438
    K = 1.0 / (1.0 + 0.2316419 * np.abs(d))
    ret_val = (RSQRT2PI * np.exp(-0.5 * d * d) *
               (K * (A1 + K * (A2 + K * (A3 + K * (A4 + K * A5))))))
    return np.where(d > 0, 1.0 - ret_val, ret_val)

    # SPEEDTIP: Despite the memory overhead and redundant computation, the above
    # is much faster than:
    #
    # for i in range(len(d)):
    #     if d[i] > 0:
    #         ret_val[i] = 1.0 - ret_val[i]
    # return ret_val


def scholes(inputs: Quote_In):
    S = inputs.spot_px
    X = inputs.strike_price
    T = inputs.t
    R = inputs.interest
    V = inputs.vol
    sqrtT = np.sqrt(T)
    d1 = (np.log(S / X) + (R + 0.5 * V * V) * T) / (V * sqrtT)
    d2 = d1 - V * sqrtT
    cndd1 = cnd(d1)
    cndd2 = cnd(d2)

    expRT = np.exp(- R * T)

    if inputs.side == SideEnum.Call:
        #Call result
        res = S * cndd1 - X * expRT * cndd2
    else:
        #Put result
        res = X * expRT * (1.0 - cndd2) - S * (1.0 - cndd1)

    return Quote_Out(price=res)

# Sample data
# def scholes(inputs: Quote_In):
#     return Quote_Out(price=1.2, delta=1, gamma=2, theta=3, vega=4, rho=5)

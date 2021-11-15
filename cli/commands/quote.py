import asyncio
import socket
import typing
import json

from termcolor import cprint

from nubia import argument, command

import requests


@command
class Sucden:
    "This is a super command"

    def __init__(self) -> None:
        self._quote_inputs = None

    @command
    @argument("side", choices=["Call", "Put"])
    @argument("spot_px")
    @argument("strike_price")
    @argument("interest")
    @argument("vol")
    @argument("t")
    def quote(self, spot_px: float, strike_price: float, interest: float, vol: float, t: float, side: typing.Optional[str] = None):
        """
        Get a quote
        """

        if side:
            q_in_call = {'side': side,
                    'spot_px': spot_px,
                    'strike_price': strike_price,
                    'interest': interest,
                    't': t,
                    'vol': vol,
                    'dividend': 0 }

            r_call = requests.post("http://localhost:8000/quote", data=json.dumps(q_in_call))
            cprint("Price for {}: {}".format(side, r_call.json()['price']))
        else:
            q_in_call = {'side': 'Call',
                    'spot_px': spot_px,
                    'strike_price': strike_price,
                    'interest': interest,
                    't': t,
                    'vol': vol,
                    'dividend': 0 }
            q_in_put = {'side': 'Put',
                    'spot_px': spot_px,
                    'strike_price': strike_price,
                    'interest': interest,
                    't': t,
                    'vol': vol,
                    'dividend': 0 }

            r_call = requests.post("http://localhost:8000/quote", data=json.dumps(q_in_call))
            r_put = requests.post("http://localhost:8000/quote", data=json.dumps(q_in_put))
            cprint("Price for {}: {}".format("Call", r_call.json()['price']))
            cprint("Price for {}: {}".format("Put", r_put.json()['price']))



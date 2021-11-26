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

    @command
    @argument("side", choices=["Call", "Put"])
    @argument("basis")
    @argument("strike_price")
    @argument("interest")
    @argument("vol")
    @argument("maturity")
    @argument("dividend")
    def quote(self, basis: float, strike_price: float, interest: float, vol: float, maturity: float, dividend: float, side: typing.Optional[str] = None):
        """
        Get a quote
        """

        if side:
            q_in_call = {'side': side,
                    'basis': basis,
                    'strike_price': strike_price,
                    'interest': interest,
                    'maturity': maturity,
                    'vol': vol,
                    'dividend': 0}

            r_call = requests.post("http://localhost:8000/quote", data=json.dumps(q_in_call))
            cprint("Price for {}: {}".format(side, r_call.json()['price']))
        else:
            q_in_call = {'side': 'Call',
                    'basis': basis,
                    'strike_price': strike_price,
                    'interest': interest,
                    'maturity': maturity,
                    'vol': vol,
                    'dividend': 0}
            q_in_put = {'side': 'Put',
                    'basis': basis,
                    'strike_price': strike_price,
                    'interest': interest,
                    'maturity': maturity,
                    'vol': vol,
                    'dividend': 0}

            r_call = requests.post("http://localhost:8000/quote", data=json.dumps(q_in_call))
            r_put = requests.post("http://localhost:8000/quote", data=json.dumps(q_in_put))
            cprint("Price for {}: {}".format("Call", r_call.json()['price']))
            cprint("Price for {}: {}".format("Put", r_put.json()['price']))



    @command
    def quotes(self):
        """
        Get all quotes
        """
        r = requests.get("http://localhost:8000/quotes")
        r_json = r.json()

        for q in r_json:
            cprint("Quote: {}".format(q))

    @command
    @argument("created_by")
    @argument("side", choices=["Call", "Put"])
    @argument("basis")
    @argument("strike_price")
    @argument("vol")
    @argument("interest")
    @argument("dividend")
    @argument("maturity")
    def save_quote_one_line(self, created_by: str, basis: float, strike_price: float, interest: float, vol: float, maturity: float, side: str, dividend: float):
        """
        Store a quote
        """

        quote_line = { 
                'side': side,
                'basis': basis,
                'strike_price': strike_price,
                'vol': vol,
                'interest': interest,
                'maturity': maturity,
                'dividend': dividend }

        quote = {'created_by': created_by, 'quote_lines': [quote_line]}

        resp = requests.post("http://localhost:8000/save_quote", data=json.dumps(quote))

        cprint("{}".format(resp.json()))

from typing import List

from fastapi import FastAPI
import uvicorn

# import core.crud as crud
from core.calcs.scholes import scholes

import core.models.models as models

app = FastAPI()

@app.get("/")
async def root():
    return {'message': 'Hello World!'}


@app.post("/quote", response_model=models.Quote_Out)
async def quote(inputs: models.Quote_In):
    return scholes(inputs)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

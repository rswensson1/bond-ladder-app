from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from ladder_engine import build_treasury_ladder
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LadderRequest(BaseModel):
    investment_amount: float
    ladder_years: int
    reinvest: bool = False

class TreasuryAllocation(BaseModel):
    maturity: str
    allocation: float
    yield_: Optional[float]
    final_value: float

@app.post("/build-ladder", response_model=List[TreasuryAllocation])
def ladder(request: LadderRequest):
    fred_api_key = os.getenv("FRED_API_KEY")
    ladder, _ = build_treasury_ladder(request.investment_amount, request.ladder_years, request.reinvest, fred_api_key)
    return ladder

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


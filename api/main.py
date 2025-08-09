from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime
import pytz

from .bazi import compute_bazi, summarize_traits

app = FastAPI(title="SoulChat BaZi API", version="0.1.0")

# CORS for FlutterFlow web/app calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BaZiRequest(BaseModel):
    name: Optional[str] = Field(None, description="User display name")
    # ISO 8601 preferred; or pass separate fields
    birth_datetime: Optional[str] = Field(
        None, description="Birth datetime string, e.g. 1992-03-14T23:30"
    )
    birth_date: Optional[str] = Field(None, description="YYYY-MM-DD (if not using birth_datetime)")
    birth_time: Optional[str] = Field(None, description="HH:mm (24h) (if not using birth_datetime)")
    timezone: Optional[str] = Field(
        "Asia/Shanghai", description="IANA tz, e.g. Asia/Shanghai, Asia/Kuala_Lumpur"
    )
    use_true_solar_time: bool = Field(False, description="If True, apply true solar time (placeholder)")

    @validator("birth_datetime", "birth_date", "birth_time", pre=True, always=True)
    def strip_empty(cls, v):
        if isinstance(v, str) and not v.strip():
            return None
        return v

class BaZiResponse(BaseModel):
    input: Dict[str, Any]
    pillars: Dict[str, Dict[str, str]]  # year, month, day, hour -> {stem, branch}
    elements: Dict[str, Any]
    traits: Dict[str, Any]
    debug: Optional[Dict[str, Any]]

def parse_birth(req: BaZiRequest) -> datetime:
    tz = pytz.timezone(req.timezone or "Asia/Shanghai")
    if req.birth_datetime:
        try:
            naive = datetime.fromisoformat(req.birth_datetime)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid birth_datetime format (use ISO 8601)")
        return tz.localize(naive) if naive.tzinfo is None else naive.astimezone(tz)
    if not (req.birth_date and req.birth_time):
        raise HTTPException(status_code=400, detail="Provide birth_datetime or birth_date + birth_time")
    try:
        naive = datetime.fromisoformat(f"{req.birth_date}T{req.birth_time}")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid birth_date/birth_time format")
    return tz.localize(naive)

@app.post("/bazi/analyze", response_model=BaZiResponse)
async def analyze_bazi(req: BaZiRequest):
    birth_dt = parse_birth(req)
    pillars, elements, dbg = compute_bazi(birth_dt, req.use_true_solar_time)
    traits = summarize_traits(pillars, elements)
    return BaZiResponse(
        input={
            "name": req.name,
            "birth_iso": birth_dt.isoformat(),
            "timezone": req.timezone,
            "use_true_solar_time": req.use_true_solar_time,
        },
        pillars=pillars,
        elements=elements,
        traits=traits,
        debug=dbg,
    )

@app.get("/health")
async def health():
    return {"status": "ok", "version": app.version}

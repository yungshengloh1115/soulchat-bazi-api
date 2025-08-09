# SoulChat BaZi API (demo)

This is a minimal FastAPI microservice that accepts birth data and returns BaZi pillars + a trait summary.

## Local run
```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
```

## Test
```bash
curl -X POST http://localhost:8000/bazi/analyze   -H 'Content-Type: application/json'   -d '{
    "name":"Sean",
    "birth_datetime":"1992-03-14T23:30",
    "timezone":"Asia/Kuala_Lumpur"
  }'
```

## Expected response (demo)
```json
{
  "input": {"name":"Sean", "birth_iso":"...", "timezone":"Asia/Kuala_Lumpur", "use_true_solar_time":false},
  "pillars": {"year":{"stem":"…","branch":"…"}, "month":{...}, "day":{...}, "hour":{...}},
  "elements": {"dominant":"金","balance": {"木":1.0,"火":0.5,"土":0.75,"金":1.25,"水":0.5}},
  "traits": {"dominant_element":"金","core_traits":["逻辑清晰","重效率","目标导向"],"action_tip":"…"},
  "debug": {"year_idx":..., "month_idx":...}
}
```

## FlutterFlow wiring
- Create **API Call**: POST `/bazi/analyze`
- Body JSON: `{ "name": "<input>", "birth_datetime": "<iso>", "timezone": "Asia/Kuala_Lumpur" }`
- Map Response: `pillars.year.stem`, `elements.dominant`, `traits.core_traits[0]` etc.
- On success: Save to App State / pass to ChatPage.

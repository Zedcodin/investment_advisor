from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import json

app = FastAPI()

@app.get("/api/gbpusd/json")
def get_forex_json():
    try:
        # Get date range (last 365 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)

        # Download data
        data = yf.download("GBPUSD=X", start=start_date, end=end_date, interval="1d")

        if data.empty:
            raise HTTPException(status_code=404, detail="No data found.")

        # Convert to JSON records
        json_str = data.reset_index().to_json(orient='records', date_format='iso')

        # Deserialize stringified JSON to Python list
        json_data = json.loads(json_str)

        return {"status": "success", "data": json_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8018)

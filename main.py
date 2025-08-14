from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
import pandas as pd
import json
import os

app = FastAPI()

calendar_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mocks", "calendar.json")
with open(calendar_file) as f:
    calendar_events = json.load(f)


@app.get("/", response_class=HTMLResponse)
def read_root():
    return "<h1>TimeGuard is running!</h1><p>Use <a href='/docs'>/docs</a> to upload timesheets.</p>"


@app.post("/timesheets")
async def upload_timesheet(file: UploadFile = File(...)):
    try:
        # Read CSV
        df = pd.read_csv(file.file)
        # Keep only needed columns
        df = df[['date', 'start', 'end', 'project']]

        # Clean date/time columns
        df['date'] = df['date'].astype(str).str.strip().str.replace(r'[^0-9\-]', '', regex=True)
        df['start'] = df['start'].astype(str).str.strip().str.replace(r'[^0-9:]', '', regex=True)
        df['end'] = df['end'].astype(str).str.strip().str.replace(r'[^0-9:]', '', regex=True)
        df['project'] = df['project'].astype(str).str.strip()

        missing_entries = []
        extra_entries = []

        # Check missing entries
        for event in calendar_events:
            match = df[
                (df['date'] == event['date']) &
                (df['project'] == event['project']) &
                (df['start'] == event['start']) &
                (df['end'] == event['end'])
            ]
            if match.empty:
                missing_entries.append(event)

        # Check extra entries
        for _, ts_entry in df.iterrows():
            match = [e for e in calendar_events if
                     e['date'] == ts_entry['date'] and
                     e['project'] == ts_entry['project'] and
                     e['start'] == ts_entry['start'] and
                     e['end'] == ts_entry['end']]
            if not match:
                extra_entries.append(ts_entry.to_dict())

        return JSONResponse(content={"missingEntries": missing_entries, "extraEntries": extra_entries})

    except Exception as e:
        import traceback
        traceback.print_exc()  # Show full Python error in terminal
        return JSONResponse(content={"error": str(e)})

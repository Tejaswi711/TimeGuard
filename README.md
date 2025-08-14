TimeGuard – Timesheet Validator

## Aim
TimeGuard compares timesheet CSVs to calendar events and flags discrepancies.

## Features
- Upload a timesheet CSV via `/timesheets` endpoint.
- Compares CSV entries with calendar events (mock data).
- Returns JSON with `missingEntries` and `extraEntries`.

## Setup
1. Clone the repo:
   ```bash
   git clone <repo-url>
   cd TimeGuard
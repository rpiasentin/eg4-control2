# EG4 Float Control – Starter Skeleton

This starter contains **no hidden folders**.  
Use it to seed a fresh GitHub repository before creating build branches.

## Structure

```
backend/    FastAPI service (Python 3.11)
web/        Static HTML + JS UI
```

### Backend quick test

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
# open http://localhost:8000/web/index.html
```

The UI shows:
* Live battery‑voltage graph (fake data until wired up)
* Current Absorb / Float set‑points
* Action log

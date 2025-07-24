# DEMO FastAPI + PostgreSQL API

This is a minimal demo backend for testing public, secure API hosting on Render with PostgreSQL.

## Features
- FastAPI backend
- PostgreSQL database (async)
- Dummy table: `items` (id, name, value)
- API key authentication via `x-api-key` header
- CRUD endpoints: create, read, delete items

## Setup

1. **Clone repo and enter directory**

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up PostgreSQL**
- Create a database (e.g., `demo_db`)
- Update `.env` with your DB credentials (see `.env.example`)

4. **Run locally**

```bash
uvicorn main:app --reload
```

5. **API Usage**
- All endpoints require `x-api-key` header (default: `mysecretkey`)
- Example: `curl -H "x-api-key: mysecretkey" http://localhost:8000/items/`

## Deploying to Render

1. Create a new **Web Service** on Render
2. Use this directory as the source
3. Set environment variables:
   - `DATABASE_URL` (Render PostgreSQL connection string)
   - `API_KEY` (your chosen API key)
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn main:app --host 0.0.0.0 --port 10000`

## Endpoints
- `POST /items/` (params: name, value)
- `GET /items/`
- `GET /items/{item_id}`
- `DELETE /items/{item_id}`

---

**This is a demo only. Do not use in production without further security hardening.** 
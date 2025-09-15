# FastAPI Todo App

Simple Todo API with a minimal HTML frontend.

## Run locally

1. Create a virtual environment (optional but recommended)
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies
```bash
python -m pip install -r requirements.txt
```

3. Start the server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. Open the app
- API docs: http://localhost:8000/docs
- Frontend: http://localhost:8000/

## API

- POST `/todos` Create
- GET `/todos` List (search, completed, skip, limit)
- GET `/todos/{id}` Read
- PUT `/todos/{id}` Update
- PATCH `/todos/{id}/toggle` Toggle completed
- DELETE `/todos/{id}` Delete

# 1st-E-Commerce-Project-using-Django

# Taskly

## Przygotowanie

```sh
cp .env.example .env
```

## Docker

```sh
docker compose up --build -d --wait
```

Aplikacja: http://localhost:8080. API: http://localhost:8000/docs.

```sh
docker compose down
```

## Frontend

Instalacja:

```sh
cd frontend
npm ci
```

Dev — http://localhost:5173:

```sh
npm run dev
```

Storybook — http://localhost:6006:

```sh
npm run storybook
```

Testy:

```sh
npm test
```

Coverage — `frontend/coverage/index.html`:

```sh
npm run test:coverage
```

## Backend

Instalacja (z katalogu repozytorium):

```sh
python3 -m venv backend/.venv
source backend/.venv/bin/activate
python -m pip install -r backend/requirements.txt
```

Dev — http://localhost:8000/docs:

```sh
docker compose up -d --wait postgres
cd backend
python -m uvicorn app.main:app --reload
```

Testy (w `backend`, z aktywnym `.venv`):

```sh
python -m pytest
```

Coverage — `backend/coverage/html/index.html`:

```sh
python -m pytest --cov=app --cov-report=term-missing --cov-report=html
```

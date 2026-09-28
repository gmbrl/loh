# loh — Land & Cadastral Registry

A full-stack web application implementing the **Professional Authority Model** for land records management.

## Stack

| Layer | Technology |
|---|---|
| Frontend | Vue 3 · Vite · Pinia · Vue Router |
| Backend | FastAPI (Python 3.12) · SQLAlchemy 2 · Alembic |
| Database | PostgreSQL 15 |
| Auth | JWT (python-jose + passlib/bcrypt) |
| Dev | Docker Compose |

---

## Quick start (Docker)

```bash
# 1. Copy the backend env file
cp backend/.env.example backend/.env

# 2. Build and start all services
docker compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| API Docs (ReDoc) | http://localhost:8000/redoc |

Default admin account seeded on first startup:

```
Email:    admin@loh.local
Password: admin
```

> **Change the `SECRET_KEY` and admin password before any production use.**

---

## Local development (without Docker)

### Backend

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt

# Set DATABASE_URL to a running PostgreSQL instance
cp .env.example .env
# Edit .env as needed

uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server proxies `/api` → `http://backend:8000`.  
For local-only development (no Docker), change the proxy target in [`vite.config.js`](frontend/vite.config.js) to `http://localhost:8000`.

---

## Authority roles

| Role | Key capabilities |
|---|---|
| `admin` | Full access, user management |
| `surveyor` | Submit survey plans |
| `cadastral_officer` | Review surveys, create official parcels |
| `lawyer_notary` | Prepare and submit title instruments |
| `registrar` | Approve/reject title applications and encumbrances |
| `bank` | Submit mortgages |
| `tax_authority` | Submit tax liens |
| `court` | Submit court orders/seizures, substantive corrections |
| `municipality` | Submit planning restrictions and rights-of-way |
| `citizen` | Initiate title applications, submit private encumbrances, query records |

---

## Workflow overview

```
Surveyor → submits survey plan
             ↓
Cadastral Officer → approves survey plan → creates official Parcel
             ↓
Lawyer/Citizen → submits Title Application
             ↓
Registrar → examines & approves → Title registered
             ↓
Bank / Tax Authority / Court / Municipality → submits Encumbrance
             ↓
Registrar → approves Encumbrance
             ↓
Original party → releases Encumbrance
```

Corrections follow three levels (clerical → technical → substantive), each requiring increasing levels of evidence and authority.

---

## Project structure

```
loh/
├── backend/
│   ├── app/
│   │   ├── core/           # config, security, permissions/RBAC
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── schemas/        # Pydantic request/response schemas
│   │   ├── routers/        # FastAPI route handlers
│   │   ├── deps.py         # JWT dependency injection
│   │   ├── database.py     # engine + session
│   │   └── main.py         # app entry point + startup seed
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/            # Axios API client
│   │   ├── assets/         # Global CSS
│   │   ├── components/     # Shared components (StatusBadge)
│   │   ├── router/         # Vue Router routes
│   │   ├── stores/         # Pinia auth store
│   │   └── views/          # Page views per domain
│   ├── index.html
│   ├── vite.config.js
│   └── Dockerfile
└── docker-compose.yml
```

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.security import hash_password
from app.database import Base, SessionLocal, engine
from app.models import *  # noqa: F401, F403 — registers all ORM models with Base
from app.routers.auth import router as auth_router
from app.routers.auth import users_router
from app.routers.corrections import router as corrections_router
from app.routers.encumbrances import router as encumbrances_router
from app.routers.parcels import router as parcels_router
from app.routers.queries import router as queries_router
from app.routers.titles import router as titles_router


def _seed_admin(db):
    from app.models.user import User

    if not db.query(User).filter(User.email == settings.FIRST_ADMIN_EMAIL).first():
        admin = User(
            email=settings.FIRST_ADMIN_EMAIL,
            full_name="System Administrator",
            hashed_password=hash_password(settings.FIRST_ADMIN_PASSWORD),
            role="admin",
        )
        db.add(admin)
        db.commit()
        print(f"[startup] Admin user created: {settings.FIRST_ADMIN_EMAIL}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        _seed_admin(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="Land & Cadastral Registry API",
    version="1.0.0",
    description="Professional authority model for land records management.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://frontend:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(parcels_router)
app.include_router(titles_router)
app.include_router(encumbrances_router)
app.include_router(corrections_router)
app.include_router(queries_router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}

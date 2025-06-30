from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, campaigns, sessions, npcs, uploads
from .database import engine
from .models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="RPG Campaign Assistant", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Svelte dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])
app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
app.include_router(npcs.router, prefix="/npcs", tags=["npcs"])
app.include_router(uploads.router, prefix="/uploads", tags=["uploads"])

@app.get("/")
async def root():
    return {"message": "RPG Campaign Assistant API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth
from app.database.db import engine
from app.database.models import Base

app = FastAPI()

# ✅ CREATE TABLES
Base.metadata.create_all(bind=engine)

# ✅ CORS FIX (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ROUTES
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/")
def home():
    return {"message": "API Running"}
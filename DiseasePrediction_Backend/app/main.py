from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth
from app.routes import stroke
from app.routes import alzheimers
from app.routes import diabetes
from app.routes import lung   # ✅ ADD THIS
from app.routes import stroke
from app.database.db import engine
from app.database.models import Base
from app.routes import migraine

from app.database.db import Base, engine
from app.database.models import *
from app.routes import analytics
Base.metadata.create_all(bind=engine)
app = FastAPI()

# ✅ CREATE TABLES
Base.metadata.create_all(bind=engine)
# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ROUTES
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(stroke.router, tags=["Stroke"])
app.include_router(diabetes.router, tags=["Diabetes"])
app.include_router(alzheimers.router, tags=["Alzheimers"])
app.include_router(lung.router, tags=["Lung"])   # ✅ THIS FIXES YOUR ISSUE
app.include_router(migraine.router, tags=["Migraine"])
app.include_router(analytics.router)
# ✅ HOME
@app.get("/")
def home():
    return {"message": "API Running"}
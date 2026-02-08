from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database import engine, Base
from app.api.routes import auth, users, channels, messages, websocket

# Import all models to ensure they're registered
from app.models import user, channel, message

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(channels.router, prefix=f"{settings.API_V1_STR}/channels", tags=["channels"])
app.include_router(messages.router, prefix=f"{settings.API_V1_STR}", tags=["messages"])
app.include_router(websocket.router, tags=["websocket"])

@app.get("/")
def root():
    return {"message": "Chat App API", "version": settings.VERSION}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

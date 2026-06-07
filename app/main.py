"""AVRY-Workflows Service"""
import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.config import settings

@asynccontextmanager
async def lifespan(app):
    print(f"[{datetime.now().isoformat()}] AVRY-Workflows starting...")
    yield
    print(f"[{datetime.now().isoformat()}] AVRY-Workflows shutting down...")

app = FastAPI(title="AVRY Workflows", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and register the proper routers (has auth, persistence, etc.)
try:
    from app.routes.workflows import router as workflows_router
    app.include_router(workflows_router)
    print("[✓] Workflows routes registered")
except Exception as e:
    print(f"[!] Could not import workflows routes: {e}")

try:
    from app.routes.n8n import router as n8n_router
    app.include_router(n8n_router)
    print("[✓] n8n routes registered")
except Exception as e:
    print(f"[!] Could not import n8n routes: {e}")

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "avry-workflows", "port": int(os.getenv("PORT", "8087")), "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/debug/info")
async def debug_info():
    return {"service": "avry-workflows", "port": int(os.getenv("PORT", "8087")), "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", settings.port or 8087))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)

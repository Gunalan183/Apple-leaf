"""
Hugging Face Spaces Entry Point
Combines FastAPI backend with React frontend
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.app.main import app as backend_app

# Create main app
app = FastAPI(title="Apple Leaf Disease Classifier")

# Mount backend API
app.mount("/api", backend_app)

# Mount frontend static files (after building)
frontend_build = Path(__file__).parent / "frontend" / "dist"
if frontend_build.exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_build / "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve React frontend"""
        file_path = frontend_build / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        # Return index.html for client-side routing
        return FileResponse(frontend_build / "index.html")
else:
    @app.get("/")
    async def root():
        return {
            "message": "Apple Leaf Disease Classifier API",
            "docs": "/docs",
            "status": "Frontend not built. Run: cd frontend && npm run build"
        }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)

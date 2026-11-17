"""
GAN-Sim-GAN FastAPI Application
Main application entry point
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Based Apple Leaf Disease Classification Using Generative Data Augmentation",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Model path: {settings.MODEL_PATH}")
    logger.info(f"Device: {settings.DEVICE}")
    
    # Don't load model at startup to save memory
    # It will be loaded on first prediction request
    app.state.classifier = None
    logger.info("✓ Application started (model will load on demand)")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    logger.info(f"Shutting down {settings.APP_NAME}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "message": "GAN-Sim-GAN API - Apple Leaf Disease Classification",
        "docs": "/docs",
        "health": "/api/health"
    }


@app.get("/api/health")
async def health_check(request: Request):
    """
    Health check endpoint
    Returns backend status and model availability
    """
    
    model_loaded = hasattr(request.app.state, 'classifier') and request.app.state.classifier is not None
    
    health_status = {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "model_loaded": model_loaded
    }
    
    if model_loaded:
        try:
            classifier = request.app.state.classifier
            model_info = classifier.get_model_info()
            health_status["model_info"] = {
                "name": model_info["model_name"],
                "accuracy": f"{model_info['validation_accuracy']:.2%}",
                "device": model_info["device"]
            }
        except:
            pass
    
    return health_status


# Include prediction routes
from app.routes.prediction import router as prediction_router
app.include_router(prediction_router)

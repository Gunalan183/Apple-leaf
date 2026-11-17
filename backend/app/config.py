"""
GAN-Sim-GAN Backend Configuration
Handles application settings and environment variables
"""

import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application Info
    APP_NAME: str = "GAN-Sim-GAN"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS Settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",  # Vite default
        "http://localhost:3000",  # React default
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]
    
    # Model Settings
    MODEL_ARCHITECTURE: str = "densenet121"
    NUM_CLASSES: int = 3
    IMAGE_SIZE: int = 224
    CLASS_NAMES: List[str] = ["scab", "rust", "healthy"]
    
    # File paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    MODEL_PATH: Path = BASE_DIR.parent / "ml-training" / "checkpoints" / "densenet121_best.pth"
    METRICS_PATH: Path = BASE_DIR.parent / "ml-training" / "reports" / "evaluation_metrics.json"
    
    # Upload Settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png"]
    
    # Device Settings
    DEVICE: str = "auto"  # Will auto-detect CUDA/CPU
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()


# Disease information dictionary
DISEASE_INFO = {
    "scab": {
        "name": "Apple Scab",
        "scientific_name": "Venturia inaequalis",
        "description": "Apple scab is a fungal disease that causes dark, olive-green to black lesions on leaves and fruit. It thrives in cool, wet conditions and can severely impact fruit quality and tree health.",
        "symptoms": [
            "Dark olive-green to black lesions on leaves",
            "Scabby lesions on fruit surface",
            "Premature leaf drop in severe cases",
            "Reduced fruit quality and marketability"
        ],
        "management": [
            "Apply fungicides during susceptible periods",
            "Remove fallen leaves to reduce overwintering inoculum",
            "Plant resistant apple varieties",
            "Ensure good air circulation through proper pruning",
            "Monitor weather conditions for infection periods"
        ],
        "severity": "High"
    },
    "rust": {
        "name": "Apple Rust",
        "scientific_name": "Gymnosporangium spp.",
        "description": "Apple rust is caused by several fungal species that require two host plants (apple and juniper) to complete their life cycle. It appears as bright orange-rust colored spots on leaves.",
        "symptoms": [
            "Bright orange to rust-colored spots on upper leaf surface",
            "Yellow spots or lesions on leaves",
            "Tube-like structures on leaf undersides",
            "Premature leaf drop in severe infections",
            "Reduced photosynthesis capacity"
        ],
        "management": [
            "Remove nearby juniper hosts if possible",
            "Apply appropriate fungicides during spring",
            "Plant rust-resistant apple varieties",
            "Remove infected leaves during growing season",
            "Maintain tree vigor through proper nutrition"
        ],
        "severity": "Moderate to High"
    },
    "healthy": {
        "name": "Healthy Leaf",
        "scientific_name": "N/A",
        "description": "A healthy apple leaf shows no signs of disease or stress. It has uniform green color, no lesions, spots, or discoloration, and maintains proper structure and function.",
        "symptoms": [
            "Uniform green coloration",
            "No visible lesions or spots",
            "Proper leaf structure and shape",
            "No premature yellowing or browning",
            "Good turgor and firmness"
        ],
        "management": [
            "Maintain regular monitoring for early disease detection",
            "Practice integrated pest management",
            "Ensure proper irrigation and nutrition",
            "Continue preventive fungicide applications as needed",
            "Maintain good orchard sanitation"
        ],
        "severity": "None"
    }
}


def get_disease_info(class_name: str) -> dict:
    """
    Get disease information for a given class
    
    Args:
        class_name: Name of the disease class
        
    Returns:
        Dictionary containing disease information
    """
    return DISEASE_INFO.get(class_name.lower(), {
        "name": "Unknown",
        "description": "No information available",
        "symptoms": [],
        "management": [],
        "severity": "Unknown"
    })

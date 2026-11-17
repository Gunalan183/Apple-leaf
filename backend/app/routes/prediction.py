"""
Prediction API Routes
Handles image upload and disease prediction
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["prediction"])


@router.post("/predict")
async def predict_disease(
    request: Request,
    file: UploadFile = File(..., description="Apple leaf image file")
):
    """
    Predict disease from uploaded leaf image
    
    - **file**: Image file (JPEG, PNG)
    - Returns disease classification with confidence scores
    """
    
    # Check if classifier is loaded
    if not hasattr(request.app.state, 'classifier') or request.app.state.classifier is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please ensure the trained model checkpoint exists."
        )
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Please upload an image file."
        )
    
    try:
        # Read image file
        contents = await file.read()
        
        # Validate image can be opened
        try:
            image = Image.open(io.BytesIO(contents))
            image.verify()  # Verify it's a valid image
            image = Image.open(io.BytesIO(contents))  # Reopen after verify
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid or corrupted image file: {str(e)}"
            )
        
        # Perform prediction
        classifier = request.app.state.classifier
        prediction = classifier.predict(image)
        
        # Add metadata
        result = {
            "success": True,
            "prediction": prediction,
            "metadata": {
                "filename": file.filename,
                "image_size": f"{image.size[0]}x{image.size[1]}",
                "image_mode": image.mode
            }
        }
        
        logger.info(f"Prediction: {prediction['class']} ({prediction['confidence']:.2%}) for {file.filename}")
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@router.get("/model/info")
async def get_model_info(request: Request):
    """
    Get model information and metadata
    
    Returns model details, classes, and performance metrics
    """
    
    if not hasattr(request.app.state, 'classifier') or request.app.state.classifier is None:
        return {
            "success": False,
            "error": "Model not loaded",
            "message": "Trained model checkpoint not found"
        }
    
    try:
        classifier = request.app.state.classifier
        info = classifier.get_model_info()
        
        return {
            "success": True,
            "model": info
        }
    
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve model info: {str(e)}"
        )


@router.get("/classes")
async def get_classes():
    """
    Get available disease classes
    
    Returns list of disease classes the model can detect
    """
    from app.models.disease_classifier import DiseaseClassifier
    
    return {
        "success": True,
        "classes": DiseaseClassifier.CLASS_NAMES,
        "display_names": DiseaseClassifier.CLASS_DISPLAY_NAMES,
        "count": len(DiseaseClassifier.CLASS_NAMES)
    }

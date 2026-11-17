"""
Disease Classification Model
Loads trained DenseNet121 and performs inference
"""

import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
import io


class DiseaseClassifier:
    """Apple Leaf Disease Classifier using trained DenseNet121"""
    
    # Class names and indices
    CLASS_NAMES = ['healthy', 'rust', 'scab']
    CLASS_DISPLAY_NAMES = {
        'healthy': 'Healthy',
        'rust': 'Apple Rust',
        'scab': 'Apple Scab'
    }
    
    def __init__(self, model_path: str, device: str = None):
        """
        Initialize the classifier
        
        Args:
            model_path: Path to trained model checkpoint (.pth file)
            device: Device to run inference on ('cuda', 'cpu', or None for auto)
        """
        self.model_path = Path(model_path)
        
        # Set device
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)
        
        # Load model
        self.model = self._load_model()
        self.model.eval()
        
        # Setup transforms
        self.transform = self._get_transform()
        
        print(f"✓ Disease classifier loaded on {self.device}")
        print(f"✓ Model: {self.model_path.name}")
        print(f"✓ Classes: {', '.join(self.CLASS_NAMES)}")
    
    def _load_model(self) -> nn.Module:
        """Load trained DenseNet121 model"""
        
        # Create model architecture
        model = models.densenet121(weights=None)
        num_features = model.classifier.in_features
        model.classifier = nn.Linear(num_features, len(self.CLASS_NAMES))
        
        # Load trained weights
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model checkpoint not found: {self.model_path}")
        
        checkpoint = torch.load(self.model_path, map_location=self.device, weights_only=False)
        model.load_state_dict(checkpoint['model_state_dict'])
        
        model = model.to(self.device)
        return model
    
    def _get_transform(self) -> transforms.Compose:
        """Get image preprocessing transforms"""
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    
    def preprocess_image(self, image: Image.Image) -> torch.Tensor:
        """
        Preprocess image for model input
        
        Args:
            image: PIL Image
            
        Returns:
            Preprocessed tensor
        """
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Apply transforms
        tensor = self.transform(image)
        
        # Add batch dimension
        tensor = tensor.unsqueeze(0)
        
        return tensor
    
    @torch.no_grad()
    def predict(self, image: Image.Image) -> Dict:
        """
        Predict disease class for an image
        
        Args:
            image: PIL Image of apple leaf
            
        Returns:
            Dictionary with prediction results:
            {
                'class': str,              # Predicted class name
                'class_display': str,      # Display name
                'confidence': float,       # Confidence (0-1)
                'probabilities': dict,     # All class probabilities
                'is_diseased': bool       # Whether leaf is diseased
            }
        """
        
        # Preprocess
        input_tensor = self.preprocess_image(image).to(self.device)
        
        # Forward pass
        outputs = self.model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        
        # Get prediction
        confidence, predicted_idx = torch.max(probabilities, 1)
        predicted_class = self.CLASS_NAMES[predicted_idx.item()]
        confidence_value = confidence.item()
        
        # Build probability dictionary
        prob_dict = {
            self.CLASS_NAMES[i]: float(probabilities[0][i].item())
            for i in range(len(self.CLASS_NAMES))
        }
        
        # Determine if diseased
        is_diseased = predicted_class != 'healthy'
        
        result = {
            'class': predicted_class,
            'class_display': self.CLASS_DISPLAY_NAMES[predicted_class],
            'confidence': confidence_value,
            'probabilities': prob_dict,
            'is_diseased': is_diseased
        }
        
        return result
    
    def predict_from_bytes(self, image_bytes: bytes) -> Dict:
        """
        Predict from image bytes (e.g., uploaded file)
        
        Args:
            image_bytes: Image file bytes
            
        Returns:
            Prediction results dictionary
        """
        image = Image.open(io.BytesIO(image_bytes))
        return self.predict(image)
    
    def predict_from_path(self, image_path: str) -> Dict:
        """
        Predict from image file path
        
        Args:
            image_path: Path to image file
            
        Returns:
            Prediction results dictionary
        """
        image = Image.open(image_path)
        return self.predict(image)
    
    def get_model_info(self) -> Dict:
        """Get model metadata"""
        
        checkpoint = torch.load(self.model_path, map_location='cpu', weights_only=False)
        
        return {
            'model_name': 'DenseNet121',
            'num_classes': len(self.CLASS_NAMES),
            'classes': self.CLASS_NAMES,
            'class_display_names': self.CLASS_DISPLAY_NAMES,
            'trained_epoch': checkpoint.get('epoch', 'unknown'),
            'validation_accuracy': float(checkpoint.get('val_acc', 0)),
            'device': str(self.device),
            'checkpoint_path': str(self.model_path)
        }


def load_classifier(model_path: str = None) -> DiseaseClassifier:
    """
    Convenience function to load the classifier
    
    Args:
        model_path: Path to model checkpoint (uses best augmented model by default)
        
    Returns:
        Initialized DiseaseClassifier
    """
    if model_path is None:
        # Default to best augmented model
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        model_path = base_dir / "ml-training" / "checkpoints" / "densenet121_augmented_best.pth"
        
        # Fallback to baseline if augmented not available
        if not model_path.exists():
            model_path = base_dir / "ml-training" / "checkpoints" / "densenet121_best.pth"
    
    return DiseaseClassifier(str(model_path))

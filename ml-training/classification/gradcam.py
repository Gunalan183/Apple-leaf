"""
GAN-Sim-GAN Grad-CAM Implementation
Gradient-weighted Class Activation Mapping for model explainability
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from classification.config import *
from classification.model import create_model, load_checkpoint
from classification.transforms import get_inference_transform, denormalize


class GradCAM:
    """
    Grad-CAM: Gradient-weighted Class Activation Mapping
    Visualizes which regions of an image are important for classification
    """
    
    def __init__(self, model, target_layer):
        """
        Args:
            model: PyTorch model
            target_layer: Target layer for Grad-CAM (usually last conv layer)
        """
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        
        # Register hooks
        self.target_layer.register_forward_hook(self.save_activation)
        self.target_layer.register_full_backward_hook(self.save_gradient)
    
    def save_activation(self, module, input, output):
        """Hook to save forward activations"""
        self.activations = output.detach().clone()
    
    def save_gradient(self, module, grad_input, grad_output):
        """Hook to save backward gradients"""
        self.gradients = grad_output[0].detach().clone()
    
    def generate_cam(self, input_tensor, target_class=None):
        """
        Generate Grad-CAM heatmap
        
        Args:
            input_tensor: Input image tensor (1, C, H, W)
            target_class: Target class index (if None, use predicted class)
            
        Returns:
            numpy array: Grad-CAM heatmap
        """
        # Forward pass
        self.model.eval()
        input_tensor.requires_grad = True
        
        with torch.set_grad_enabled(True):
            output = self.model(input_tensor)
        
        # Get target class
        if target_class is None:
            target_class = output.argmax(dim=1).item()
        
        # Backward pass
        self.model.zero_grad()
        if input_tensor.grad is not None:
            input_tensor.grad.zero_()
        
        class_loss = output[0, target_class]
        class_loss.backward(retain_graph=False)
        
        # Get gradients and activations
        if self.gradients is None or self.activations is None:
            return np.zeros((7, 7), dtype=np.float32), target_class
            
        gradients = self.gradients[0].cpu().numpy()  # (C, H, W)
        activations = self.activations[0].cpu().numpy()  # (C, H, W)
        
        # Calculate weights (global average pooling of gradients)
        weights = np.mean(gradients, axis=(1, 2))  # (C,)
        
        # Generate Grad-CAM
        cam = np.zeros(activations.shape[1:], dtype=np.float32)  # (H, W)
        
        for i, w in enumerate(weights):
            cam += w * activations[i]
        
        # Apply ReLU (only positive contributions)
        cam = np.maximum(cam, 0)
        
        # Normalize
        if cam.max() > 0:
            cam = cam / cam.max()
        
        return cam, target_class
    
    def __call__(self, input_tensor, target_class=None):
        """Shortcut for generate_cam"""
        return self.generate_cam(input_tensor, target_class)


def get_target_layer(model, model_name='densenet121'):
    """
    Get the target layer for Grad-CAM
    
    Args:
        model: PyTorch model
        model_name: Model architecture name
        
    Returns:
        Target layer for Grad-CAM
    """
    if model_name.lower() == 'densenet121':
        # For DenseNet, use the last layer of features
        return model.features[-1]
    else:
        raise ValueError(f"Unsupported model for Grad-CAM: {model_name}")


def overlay_heatmap(image, heatmap, alpha=0.4, colormap=cv2.COLORMAP_JET):
    """
    Overlay heatmap on original image
    
    Args:
        image: Original image (H, W, 3) in range [0, 1]
        heatmap: Grad-CAM heatmap (H, W) in range [0, 1]
        alpha: Transparency of heatmap
        colormap: OpenCV colormap
        
    Returns:
        numpy array: Overlaid image
    """
    # Resize heatmap to match image size
    heatmap_resized = cv2.resize(heatmap, (image.shape[1], image.shape[0]))
    
    # Apply colormap
    heatmap_colored = cv2.applyColorMap(
        (heatmap_resized * 255).astype(np.uint8),
        colormap
    )
    heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
    heatmap_colored = heatmap_colored.astype(np.float32) / 255
    
    # Overlay
    overlaid = (1 - alpha) * image + alpha * heatmap_colored
    overlaid = np.clip(overlaid, 0, 1)
    
    return overlaid


def visualize_gradcam(image_path, model, device, class_names, save_path=None):
    """
    Generate and visualize Grad-CAM for an image
    
    Args:
        image_path: Path to input image
        model: Trained PyTorch model
        device: Device to run on
        class_names: List of class names
        save_path: Path to save visualization (optional)
        
    Returns:
        tuple: (prediction, confidence, gradcam_image)
    """
    # Load and preprocess image
    original_image = Image.open(image_path).convert('RGB')
    original_array = np.array(original_image).astype(np.float32) / 255
    
    transform = get_inference_transform()
    input_tensor = transform(original_image).unsqueeze(0).to(device)
    
    # Get target layer
    target_layer = get_target_layer(model, MODEL_NAME)
    
    # Create Grad-CAM
    gradcam = GradCAM(model, target_layer)
    
    # Generate heatmap
    heatmap, pred_class = gradcam(input_tensor)
    
    # Get prediction confidence
    with torch.no_grad():
        output = model(input_tensor)
        probs = F.softmax(output, dim=1)
        confidence = probs[0, pred_class].item()
    
    # Overlay heatmap
    overlaid = overlay_heatmap(original_array, heatmap)
    
    # Create visualization
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Original image
    axes[0].imshow(original_array)
    axes[0].set_title('Original Image', fontsize=12, fontweight='bold')
    axes[0].axis('off')
    
    # Heatmap
    axes[1].imshow(heatmap, cmap='jet')
    axes[1].set_title('Grad-CAM Heatmap', fontsize=12, fontweight='bold')
    axes[1].axis('off')
    
    # Overlaid
    axes[2].imshow(overlaid)
    axes[2].set_title(
        f'Prediction: {class_names[pred_class].capitalize()}\n'
        f'Confidence: {confidence:.2%}',
        fontsize=12, fontweight='bold'
    )
    axes[2].axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Grad-CAM visualization saved: {save_path}")
    
    plt.close()
    
    return pred_class, confidence, overlaid


def generate_gradcam_for_samples(model, data_dir, device, class_names, 
                                 num_samples=3, save_dir=None):
    """
    Generate Grad-CAM for sample images from each class
    
    Args:
        model: Trained model
        data_dir: Directory containing class subdirectories
        device: Device to run on
        class_names: List of class names
        num_samples: Number of samples per class
        save_dir: Directory to save visualizations
        
    Returns:
        dict: Results for each class
    """
    results = {}
    
    if save_dir:
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
    
    for class_name in class_names:
        class_dir = Path(data_dir) / class_name
        
        if not class_dir.exists():
            print(f"⚠️  Class directory not found: {class_dir}")
            continue
        
        # Get sample images
        image_files = list(class_dir.glob('*.[jp][pn][g]*'))
        image_files += list(class_dir.glob('*.jpeg'))
        
        if len(image_files) == 0:
            print(f"⚠️  No images found in: {class_dir}")
            continue
        
        # Sample random images
        import random
        sample_files = random.sample(image_files, min(num_samples, len(image_files)))
        
        class_results = []
        
        for idx, image_file in enumerate(sample_files):
            save_path = None
            if save_dir:
                save_path = save_dir / f"gradcam_{class_name}_{idx + 1}.png"
            
            try:
                pred_class, confidence, overlaid = visualize_gradcam(
                    image_file, model, device, class_names, save_path
                )
                
                class_results.append({
                    'image': str(image_file),
                    'predicted': class_names[pred_class],
                    'confidence': confidence,
                    'correct': (pred_class == class_names.index(class_name))
                })
            
            except Exception as e:
                print(f"❌ Error processing {image_file}: {e}")
        
        results[class_name] = class_results
    
    return results


def main():
    """Main Grad-CAM generation function"""
    print("=" * 70)
    print("GAN-SIM-GAN: GRAD-CAM VISUALIZATION")
    print("=" * 70)
    
    # Check if model exists
    if not CHECKPOINT_BEST.exists():
        print(f"\n❌ Error: Model checkpoint not found at {CHECKPOINT_BEST}")
        print("   Please train the model first by running: python train.py")
        return
    
    print(f"\n💻 Using device: {DEVICE}")
    
    # Load model
    print("\n🔨 Loading trained model...")
    model = create_model(MODEL_NAME, NUM_CLASSES, pretrained=False)
    model, epoch, val_loss, val_acc = load_checkpoint(model, CHECKPOINT_BEST, DEVICE)
    model = model.to(DEVICE)
    model.eval()
    
    # Generate Grad-CAM for test samples
    print("\n📊 Generating Grad-CAM visualizations for test samples...")
    gradcam_dir = REPORTS_DIR / "gradcam_samples"
    
    results = generate_gradcam_for_samples(
        model=model,
        data_dir=TEST_DIR,
        device=DEVICE,
        class_names=CLASS_NAMES,
        num_samples=3,
        save_dir=gradcam_dir
    )
    
    # Print summary
    print("\n" + "=" * 70)
    print("GRAD-CAM GENERATION SUMMARY")
    print("=" * 70)
    
    for class_name, class_results in results.items():
        correct = sum(1 for r in class_results if r['correct'])
        total = len(class_results)
        avg_confidence = np.mean([r['confidence'] for r in class_results])
        
        print(f"\n{class_name.capitalize()}:")
        print(f"   Samples: {total}")
        print(f"   Correct predictions: {correct}/{total}")
        print(f"   Average confidence: {avg_confidence:.2%}")
    
    print("\n" + "=" * 70)
    print("✅ GRAD-CAM GENERATION COMPLETED!")
    print("=" * 70)
    print(f"\n📁 Visualizations saved in: {gradcam_dir}")
    print("\n💡 Grad-CAM helps understand which image regions influenced the prediction")
    print("   Brighter areas indicate higher importance for the classification")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n\n❌ Grad-CAM generation failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

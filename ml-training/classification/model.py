"""
GAN-Sim-GAN Model Architecture
DenseNet121 with custom classification head
"""

import torch
import torch.nn as nn
from torchvision import models


def create_densenet121(num_classes=3, pretrained=True, freeze_features=False):
    """
    Create DenseNet121 model for classification
    
    Args:
        num_classes (int): Number of output classes
        pretrained (bool): Whether to use ImageNet pretrained weights
        freeze_features (bool): Whether to freeze feature extractor
        
    Returns:
        nn.Module: DenseNet121 model
    """
    # Load pretrained DenseNet121
    if pretrained:
        print("📥 Loading pretrained DenseNet121 weights from ImageNet...")
        model = models.densenet121(weights=models.DenseNet121_Weights.IMAGENET1K_V1)
    else:
        print("🔨 Creating DenseNet121 from scratch...")
        model = models.densenet121(weights=None)
    
    # Freeze feature extractor if specified
    if freeze_features:
        print("❄️  Freezing feature extractor layers...")
        for param in model.features.parameters():
            param.requires_grad = False
    
    # Replace classifier with custom head
    num_features = model.classifier.in_features
    model.classifier = nn.Linear(num_features, num_classes)
    
    print(f"✅ Model created with {num_classes} output classes")
    print(f"   Feature dim: {num_features}")
    
    return model


def create_model(model_name='densenet121', num_classes=3, pretrained=True):
    """
    Create model by name
    
    Args:
        model_name (str): Model architecture name
        num_classes (int): Number of output classes
        pretrained (bool): Whether to use pretrained weights
        
    Returns:
        nn.Module: Model
    """
    if model_name.lower() == 'densenet121':
        return create_densenet121(num_classes, pretrained)
    else:
        raise ValueError(f"Unsupported model: {model_name}")


def count_parameters(model):
    """
    Count total and trainable parameters
    
    Args:
        model: PyTorch model
        
    Returns:
        tuple: (total_params, trainable_params)
    """
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    
    return total_params, trainable_params


def print_model_summary(model):
    """
    Print model architecture summary
    
    Args:
        model: PyTorch model
    """
    total_params, trainable_params = count_parameters(model)
    
    print("\n" + "=" * 70)
    print("MODEL SUMMARY")
    print("=" * 70)
    print(f"Architecture: {model.__class__.__name__}")
    print(f"Total parameters: {total_params:,}")
    print(f"Trainable parameters: {trainable_params:,}")
    print(f"Non-trainable parameters: {total_params - trainable_params:,}")
    print(f"Memory footprint: ~{(total_params * 4) / (1024**2):.2f} MB")
    print("=" * 70 + "\n")


def save_checkpoint(model, optimizer, epoch, val_loss, val_acc, filepath):
    """
    Save model checkpoint
    
    Args:
        model: PyTorch model
        optimizer: Optimizer
        epoch: Current epoch
        val_loss: Validation loss
        val_acc: Validation accuracy
        filepath: Path to save checkpoint
    """
    checkpoint = {
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'val_loss': val_loss,
        'val_acc': val_acc
    }
    
    torch.save(checkpoint, filepath)
    print(f"💾 Checkpoint saved: {filepath}")


def load_checkpoint(model, filepath, device, optimizer=None):
    """
    Load model checkpoint
    
    Args:
        model: PyTorch model
        filepath: Path to checkpoint
        device: Device to load model on
        optimizer: Optimizer (optional)
        
    Returns:
        tuple: (model, optimizer, epoch, val_loss, val_acc) or (model, epoch, val_loss, val_acc)
    """
    checkpoint = torch.load(filepath, map_location=device)
    
    model.load_state_dict(checkpoint['model_state_dict'])
    epoch = checkpoint['epoch']
    val_loss = checkpoint['val_loss']
    val_acc = checkpoint['val_acc']
    
    print(f"📥 Checkpoint loaded: {filepath}")
    print(f"   Epoch: {epoch}")
    print(f"   Val Loss: {val_loss:.4f}")
    print(f"   Val Acc: {val_acc:.4f}")
    
    if optimizer is not None:
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        return model, optimizer, epoch, val_loss, val_acc
    else:
        return model, epoch, val_loss, val_acc


class ModelEMA:
    """
    Exponential Moving Average of model parameters
    Helps with model generalization
    """
    
    def __init__(self, model, decay=0.999):
        self.model = model
        self.decay = decay
        self.shadow = {}
        self.backup = {}
        
        # Initialize shadow parameters
        for name, param in model.named_parameters():
            if param.requires_grad:
                self.shadow[name] = param.data.clone()
    
    def update(self):
        """Update shadow parameters"""
        for name, param in self.model.named_parameters():
            if param.requires_grad:
                new_average = (1.0 - self.decay) * param.data + self.decay * self.shadow[name]
                self.shadow[name] = new_average.clone()
    
    def apply_shadow(self):
        """Apply shadow parameters to model"""
        for name, param in self.model.named_parameters():
            if param.requires_grad:
                self.backup[name] = param.data
                param.data = self.shadow[name]
    
    def restore(self):
        """Restore original parameters"""
        for name, param in self.model.named_parameters():
            if param.requires_grad:
                param.data = self.backup[name]
        self.backup = {}


if __name__ == "__main__":
    # Test model creation
    import sys
    from pathlib import Path
    
    sys.path.append(str(Path(__file__).parent.parent))
    from classification.config import NUM_CLASSES, DEVICE
    
    print("Testing Model Creation...")
    
    # Create model
    model = create_densenet121(num_classes=NUM_CLASSES, pretrained=True)
    model = model.to(DEVICE)
    
    # Print summary
    print_model_summary(model)
    
    # Test forward pass
    dummy_input = torch.randn(2, 3, 224, 224).to(DEVICE)
    print(f"Input shape: {dummy_input.shape}")
    
    output = model(dummy_input)
    print(f"Output shape: {output.shape}")
    print(f"Output range: [{output.min():.3f}, {output.max():.3f}]")
    
    # Test probabilities
    probs = torch.nn.functional.softmax(output, dim=1)
    print(f"Probabilities shape: {probs.shape}")
    print(f"Probabilities sum: {probs.sum(dim=1)}")
    
    print("\n✅ Model test passed!")

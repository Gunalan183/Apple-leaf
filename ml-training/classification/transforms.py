"""
GAN-Sim-GAN Data Transforms
Image preprocessing and augmentation pipelines
"""

import torch
from torchvision import transforms
from classification.config import (
    IMAGE_SIZE, 
    IMAGENET_MEAN, 
    IMAGENET_STD,
    AUGMENTATION
)


def get_transforms(image_size=IMAGE_SIZE, augment=True):
    """
    Get image transforms for training and validation
    
    Args:
        image_size (int): Target image size
        augment (bool): Whether to include augmentation (for training)
        
    Returns:
        tuple: (train_transform, val_transform)
    """
    
    # Training transforms (with augmentation)
    if augment:
        train_transform = transforms.Compose([
            transforms.Resize((image_size + 32, image_size + 32)),  # Slightly larger for crop
            transforms.RandomCrop(image_size),
            transforms.RandomHorizontalFlip(p=AUGMENTATION['horizontal_flip_prob']),
            transforms.RandomRotation(degrees=AUGMENTATION['rotation_degrees']),
            transforms.ColorJitter(
                brightness=AUGMENTATION['color_jitter']['brightness'],
                contrast=AUGMENTATION['color_jitter']['contrast'],
                saturation=AUGMENTATION['color_jitter']['saturation'],
                hue=AUGMENTATION['color_jitter']['hue']
            ),
            transforms.ToTensor(),
            transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
        ])
    else:
        # No augmentation for training
        train_transform = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
        ])
    
    # Validation/Test transforms (no augmentation)
    val_transform = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
    ])
    
    return train_transform, val_transform


def denormalize(tensor, mean=IMAGENET_MEAN, std=IMAGENET_STD):
    """
    Denormalize a tensor image for visualization
    
    Args:
        tensor: Normalized image tensor (C, H, W)
        mean: Mean used for normalization
        std: Standard deviation used for normalization
        
    Returns:
        tensor: Denormalized image tensor
    """
    mean = torch.tensor(mean).view(3, 1, 1)
    std = torch.tensor(std).view(3, 1, 1)
    
    return tensor * std + mean


def get_inference_transform(image_size=IMAGE_SIZE):
    """
    Get transform for inference (single image prediction)
    
    Args:
        image_size (int): Target image size
        
    Returns:
        transforms.Compose: Inference transform pipeline
    """
    return transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
    ])


class CustomCompose:
    """
    Custom Compose that allows accessing intermediate results
    Useful for Grad-CAM and visualization
    """
    
    def __init__(self, transforms_list):
        self.transforms = transforms_list
    
    def __call__(self, img):
        for t in self.transforms:
            img = t(img)
        return img
    
    def __repr__(self):
        format_string = self.__class__.__name__ + '('
        for t in self.transforms:
            format_string += '\n'
            format_string += f'    {t}'
        format_string += '\n)'
        return format_string


def print_transform_summary():
    """Print summary of transforms"""
    train_transform, val_transform = get_transforms()
    
    print("=" * 70)
    print("DATA TRANSFORMS")
    print("=" * 70)
    print("\n📊 Training Transforms (with augmentation):")
    print(train_transform)
    print("\n📊 Validation/Test Transforms (no augmentation):")
    print(val_transform)
    print("\n" + "=" * 70)


if __name__ == "__main__":
    # Test transforms
    from PIL import Image
    import numpy as np
    
    print("Testing Transforms...")
    
    # Create a dummy image
    dummy_image = Image.fromarray(
        np.random.randint(0, 255, (2048, 1365, 3), dtype=np.uint8)
    )
    
    print(f"Original image size: {dummy_image.size}")
    
    # Test training transform
    train_transform, val_transform = get_transforms()
    
    train_tensor = train_transform(dummy_image)
    print(f"Training transform output shape: {train_tensor.shape}")
    print(f"Training transform output range: [{train_tensor.min():.3f}, {train_tensor.max():.3f}]")
    
    # Test validation transform
    val_tensor = val_transform(dummy_image)
    print(f"Validation transform output shape: {val_tensor.shape}")
    print(f"Validation transform output range: [{val_tensor.min():.3f}, {val_tensor.max():.3f}]")
    
    # Test denormalization
    denorm_tensor = denormalize(val_tensor)
    print(f"Denormalized range: [{denorm_tensor.min():.3f}, {denorm_tensor.max():.3f}]")
    
    # Print summary
    print()
    print_transform_summary()
    
    print("\n✅ Transforms test passed!")

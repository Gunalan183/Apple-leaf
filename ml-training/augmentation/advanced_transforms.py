"""
Advanced Augmentation Transforms
Realistic augmentation using Albumentations library
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import albumentations as A
from albumentations.pytorch import ToTensorV2
import numpy as np
import cv2

# Import config
try:
    from augmentation.config import *
except ImportError:
    from config import *


def get_advanced_augmentation(intensity='medium'):
    """
    Get advanced augmentation pipeline
    
    Args:
        intensity: 'light', 'medium', or 'heavy'
        
    Returns:
        Albumentations Compose object
    """
    
    intensity_cfg = INTENSITY_LEVELS.get(intensity, INTENSITY_LEVELS['medium'])
    
    # Geometric transforms
    geometric_transforms = [
        A.Rotate(
            limit=GEOMETRIC['rotation_limit'],
            p=intensity_cfg['geometric_prob'],
            border_mode=cv2.BORDER_REFLECT
        ),
        A.ShiftScaleRotate(
            shift_limit=0.1,
            scale_limit=GEOMETRIC['scale_limit'],
            rotate_limit=0,  # Already covered by Rotate
            p=intensity_cfg['geometric_prob'],
            border_mode=cv2.BORDER_REFLECT
        ),
        A.Affine(
            shear=GEOMETRIC['shear_limit'],
            p=intensity_cfg['geometric_prob'] * 0.5,
        ),
        A.Perspective(
            scale=GEOMETRIC['perspective_scale'],
            p=intensity_cfg['geometric_prob'] * 0.3,
        ),
        A.ElasticTransform(
            alpha=GEOMETRIC['elastic_alpha'],
            sigma=GEOMETRIC['elastic_sigma'],
            p=intensity_cfg['geometric_prob'] * 0.2,
            border_mode=cv2.BORDER_REFLECT
        ),
    ]
    
    # Photometric transforms
    photometric_transforms = [
        A.RandomBrightnessContrast(
            brightness_limit=PHOTOMETRIC['brightness_limit'],
            contrast_limit=PHOTOMETRIC['contrast_limit'],
            p=intensity_cfg['photometric_prob']
        ),
        A.HueSaturationValue(
            hue_shift_limit=PHOTOMETRIC['hue_limit'],
            sat_shift_limit=int(PHOTOMETRIC['saturation_limit'] * 100),
            val_shift_limit=int(PHOTOMETRIC['brightness_limit'] * 100),
            p=intensity_cfg['photometric_prob']
        ),
        A.RandomGamma(
            gamma_limit=PHOTOMETRIC['gamma_limit'],
            p=intensity_cfg['photometric_prob'] * 0.5
        ),
        A.CLAHE(
            clip_limit=4.0,
            tile_grid_size=(8, 8),
            p=intensity_cfg['photometric_prob'] * 0.3
        ),
    ]
    
    # Image quality transforms
    quality_transforms = [
        A.OneOf([
            A.GaussianBlur(blur_limit=IMAGE_QUALITY['blur_limit'], p=1.0),
            A.MotionBlur(blur_limit=IMAGE_QUALITY['blur_limit'], p=1.0),
            A.MedianBlur(blur_limit=7, p=1.0),
        ], p=intensity_cfg['quality_prob'] * 0.4),
        
        A.GaussNoise(
            var_limit=IMAGE_QUALITY['gaussian_noise_var'][1],
            p=intensity_cfg['quality_prob'] * 0.3
        ),
        
        A.ImageCompression(
            quality_range=IMAGE_QUALITY['compression_quality'],
            p=intensity_cfg['quality_prob'] * 0.3
        ),
    ]
    
    # Environmental effects
    environmental_transforms = [
        A.RandomShadow(
            shadow_roi=(0, 0.5, 1, 1),
            num_shadows_limit=(1, 2),
            p=ENVIRONMENTAL['shadow_probability'] * intensity_cfg['environmental_prob']
        ),
        A.RandomRain(
            slant_range=(-10, 10),
            drop_length=20,
            drop_width=1,
            p=ENVIRONMENTAL['rain_probability'] * intensity_cfg['environmental_prob']
        ),
        A.RandomSunFlare(
            flare_roi=(0, 0, 1, 0.5),
            angle_range=(0, 1),
            num_flare_circles_range=(1, 2),
            p=ENVIRONMENTAL['sunflare_probability'] * intensity_cfg['environmental_prob']
        ),
    ]
    
    # Additional realistic augmentations
    additional_transforms = [
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.2),
        A.Transpose(p=0.1),
        A.RandomGridShuffle(grid=(2, 2), p=0.1),  # Subtle local shuffling
    ]
    
    # Combine all transforms
    transform_list = (
        geometric_transforms +
        photometric_transforms +
        quality_transforms +
        environmental_transforms +
        additional_transforms
    )
    
    # Final composition
    augmentation = A.Compose(transform_list)
    
    return augmentation


def get_test_augmentation():
    """
    Get a simple test augmentation to verify pipeline
    
    Returns:
        Alb umentations Compose object
    """
    return A.Compose([
        A.Rotate(limit=15, p=1.0),
        A.RandomBrightnessContrast(p=1.0),
        A.HorizontalFlip(p=0.5),
    ])


def validate_augmented_image(image):
    """
    Validate if augmented image passes quality control
    
    Args:
        image: numpy array (H, W, C) in RGB format
        
    Returns:
        bool: True if image passes quality control
    """
    if not QUALITY_CONTROL['validate_realistic']:
        return True
    
    # Convert to grayscale for analysis
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    # Check brightness
    mean_brightness = np.mean(gray)
    if mean_brightness < QUALITY_CONTROL['min_brightness'] or \
       mean_brightness > QUALITY_CONTROL['max_brightness']:
        return False
    
    # Check contrast
    contrast = np.std(gray)
    if contrast < QUALITY_CONTROL['min_contrast']:
        return False
    
    # Check blur (Laplacian variance)
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
    if blur_score < QUALITY_CONTROL['max_blur_score']:
        return False
    
    return True


class AugmentationConfig:
    """
    Wrapper class for augmentation configuration
    Allows easy access to augmentation pipelines
    """
    
    def __init__(self):
        self.light = get_advanced_augmentation('light')
        self.medium = get_advanced_augmentation('medium')
        self.heavy = get_advanced_augmentation('heavy')
        self.test = get_test_augmentation()
    
    def get_random_intensity(self):
        """Get random augmentation based on intensity distribution"""
        intensities = list(INTENSITY_DISTRIBUTION.keys())
        probabilities = list(INTENSITY_DISTRIBUTION.values())
        
        chosen = np.random.choice(intensities, p=probabilities)
        return getattr(self, chosen)


def test_augmentation():
    """
    Test the augmentation pipeline
    """
    import sys
    from pathlib import Path
    from PIL import Image
    import matplotlib.pyplot as plt
    
    print("=" * 70)
    print("TESTING AUGMENTATION PIPELINE")
    print("=" * 70)
    
    # Find a sample image
    dataset_dir = BASE_DIR / "datasets" / "Apple" / "train"
    sample_classes = ['scab', 'rust', 'healthy']
    
    for class_name in sample_classes:
        class_dir = dataset_dir / class_name
        if not class_dir.exists():
            continue
        
        images = list(class_dir.glob('*.jpg'))
        if not images:
            continue
        
        # Load first image
        img_path = images[0]
        image = np.array(Image.open(img_path).convert('RGB'))
        
        print(f"\nTesting on: {img_path.name}")
        print(f"Original shape: {image.shape}")
        
        # Test different intensities
        config = AugmentationConfig()
        
        fig, axes = plt.subplots(2, 4, figsize=(16, 8))
        fig.suptitle(f'Augmentation Test - {class_name.capitalize()}', fontsize=16)
        
        # Original
        axes[0, 0].imshow(image)
        axes[0, 0].set_title('Original')
        axes[0, 0].axis('off')
        
        # Light
        aug_light = config.light(image=image)['image']
        axes[0, 1].imshow(aug_light)
        axes[0, 1].set_title('Light Intensity')
        axes[0, 1].axis('off')
        
        # Medium
        aug_medium = config.medium(image=image)['image']
        axes[0, 2].imshow(aug_medium)
        axes[0, 2].set_title('Medium Intensity')
        axes[0, 2].axis('off')
        
        # Heavy
        aug_heavy = config.heavy(image=image)['image']
        axes[0, 3].imshow(aug_heavy)
        axes[0, 3].set_title('Heavy Intensity')
        axes[0, 3].axis('off')
        
        # More examples with random intensity
        for i in range(4):
            aug = config.get_random_intensity()(image=image)['image']
            axes[1, i].imshow(aug)
            axes[1, i].set_title(f'Random {i+1}')
            axes[1, i].axis('off')
        
        plt.tight_layout()
        
        # Save
        output_path = REPORTS_DIR / f'augmentation_test_{class_name}.png'
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"Saved test visualization: {output_path}")
        
        # Test validation
        print("\nQuality control test:")
        for intensity in ['light', 'medium', 'heavy']:
            aug_pipeline = getattr(config, intensity)
            aug_img = aug_pipeline(image=image)['image']
            is_valid = validate_augmented_image(aug_img)
            print(f"  {intensity.capitalize()}: {'✅ PASS' if is_valid else '❌ FAIL'}")
        
        break  # Only test first class
    
    print("\n" + "=" * 70)
    print("✅ AUGMENTATION TEST COMPLETED")
    print("=" * 70)


if __name__ == '__main__':
    import sys
    
    if '--test' in sys.argv:
        test_augmentation()
    else:
        print("Usage: python advanced_transforms.py --test")
        print("This will test the augmentation pipeline on sample images")

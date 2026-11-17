"""
Augmentation Configuration
Controls advanced augmentation parameters for synthetic data generation
"""

from pathlib import Path

# Directories
BASE_DIR = Path(__file__).resolve().parent.parent
ORIGINAL_DATASET = BASE_DIR / "datasets" / "Apple"
AUGMENTED_DATASET = BASE_DIR / "datasets" / "Apple_Augmented"
REPORTS_DIR = BASE_DIR / "reports" / "augmentation_analysis"

# Create directories
AUGMENTED_DATASET.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Augmentation Strategy
AUGMENTATION_FACTOR = 2  # Generate 2x synthetic samples (2,420 new images)
TARGET_TRAIN_SIZE = 3630  # 1,210 original + 2,420 synthetic

# Class Distribution (target)
CLASS_TARGETS = {
    'scab': 1242,   # 414 * 3
    'rust': 1305,   # 435 * 3
    'healthy': 1083  # 361 * 3
}

# Image Settings
IMAGE_SIZE = 224
SAVE_QUALITY = 95  # JPEG quality for saved images

# Augmentation Parameters

# Geometric Transformations
GEOMETRIC = {
    'rotation_limit': 30,        # ±30 degrees
    'scale_limit': 0.2,          # 0.8x to 1.2x
    'shear_limit': 15,           # ±15 degrees shear
    'perspective_scale': 0.05,   # Perspective distortion
    'elastic_alpha': 120,        # Elastic deformation strength
    'elastic_sigma': 120 * 0.05  # Elastic deformation smoothness
}

# Photometric Transformations
PHOTOMETRIC = {
    'brightness_limit': 0.3,     # ±30% brightness
    'contrast_limit': 0.3,       # ±30% contrast
    'saturation_limit': 0.3,     # ±30% saturation
    'hue_limit': 20,             # ±20 hue shift
    'gamma_limit': (80, 120),    # Gamma correction range
}

# Image Quality Augmentation
IMAGE_QUALITY = {
    'blur_limit': 7,             # Max blur kernel size
    'gaussian_noise_var': (10, 50),  # Noise variance range
    'compression_quality': (75, 100), # JPEG compression quality
}

# Weather/Environmental Effects
ENVIRONMENTAL = {
    'rain_probability': 0.1,     # 10% chance of rain effect
    'shadow_probability': 0.3,   # 30% chance of shadows
    'sunflare_probability': 0.05 # 5% chance of sun flare
}

# Augmentation Intensity Levels
# Each sample gets one of these intensity levels randomly
INTENSITY_LEVELS = {
    'light': {
        'geometric_prob': 0.5,
        'photometric_prob': 0.7,
        'quality_prob': 0.3,
        'environmental_prob': 0.1
    },
    'medium': {
        'geometric_prob': 0.7,
        'photometric_prob': 0.8,
        'quality_prob': 0.5,
        'environmental_prob': 0.2
    },
    'heavy': {
        'geometric_prob': 0.9,
        'photometric_prob': 0.9,
        'quality_prob': 0.7,
        'environmental_prob': 0.3
    }
}

# Distribution of intensity levels
INTENSITY_DISTRIBUTION = {
    'light': 0.3,    # 30% light augmentation
    'medium': 0.5,   # 50% medium augmentation
    'heavy': 0.2     # 20% heavy augmentation
}

# Quality Control
QUALITY_CONTROL = {
    'min_brightness': 10,        # Minimum mean brightness
    'max_brightness': 245,       # Maximum mean brightness
    'min_contrast': 5,           # Minimum std deviation
    'max_blur_score': 50,        # Maximum blur score (lower = blurrier)
    'validate_realistic': True   # Apply realism checks
}

# Random Seed
RANDOM_SEED = 42

# Visualization Settings
VIS_SAMPLES_PER_CLASS = 5  # Number of samples to visualize
VIS_GRID_SIZE = (5, 3)     # Grid layout for visualization

# Processing
BATCH_SIZE = 32  # For batch processing
NUM_WORKERS = 4  # Parallel workers (0 = main thread)

# Output Format
SAVE_FORMAT = 'jpg'  # Image format for synthetic samples
NAMING_PATTERN = '{class_name}_aug_{original}_{index:04d}.jpg'  # Naming convention

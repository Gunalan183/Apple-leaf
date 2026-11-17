"""
GAN-Sim-GAN Classification Configuration
Central configuration for model training
"""

import torch
from pathlib import Path

# Directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATASETS_DIR = BASE_DIR / "datasets" / "Apple_Augmented"  # Using augmented dataset
CHECKPOINTS_DIR = BASE_DIR / "checkpoints"
REPORTS_DIR = BASE_DIR / "reports"

# Dataset Configuration
CLASS_NAMES = ['scab', 'rust', 'healthy']
NUM_CLASSES = len(CLASS_NAMES)
IMAGE_SIZE = 224

# Data Split Paths
TRAIN_DIR = DATASETS_DIR / "train"
VAL_DIR = DATASETS_DIR / "validation"
TEST_DIR = DATASETS_DIR / "test"

# Training Hyperparameters
BATCH_SIZE = 8  # Reduced from 32 for low-memory systems
NUM_EPOCHS = 50
LEARNING_RATE = 0.001
WEIGHT_DECAY = 1e-4

# Model Configuration
MODEL_NAME = "densenet121"
PRETRAINED = True

# Device Configuration
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Random Seed for Reproducibility
RANDOM_SEED = 42

# Data Augmentation Settings
AUGMENTATION = {
    'rotation_degrees': 15,
    'horizontal_flip_prob': 0.5,
    'color_jitter': {
        'brightness': 0.2,
        'contrast': 0.2,
        'saturation': 0.2,
        'hue': 0.1
    }
}

# Training Settings
EARLY_STOPPING_PATIENCE = 10
SAVE_BEST_MODEL = True
NUM_WORKERS = 0  # Set to 0 to disable multiprocessing (uses main thread only)

# Learning Rate Scheduler
LR_SCHEDULER = {
    'type': 'ReduceLROnPlateau',
    'mode': 'min',
    'factor': 0.5,
    'patience': 5,
    'min_lr': 1e-6
}

# ImageNet Normalization (for pretrained models)
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

# Checkpoint Naming
CHECKPOINT_BEST = CHECKPOINTS_DIR / f"{MODEL_NAME}_augmented_best.pth"
CHECKPOINT_LATEST = CHECKPOINTS_DIR / f"{MODEL_NAME}_augmented_latest.pth"
TRAINING_HISTORY = REPORTS_DIR / "training_history_augmented.json"

# Create directories if they don't exist
CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def print_config():
    """Print configuration summary"""
    print("=" * 70)
    print("GAN-SIM-GAN: TRAINING CONFIGURATION")
    print("=" * 70)
    print(f"\nModel: {MODEL_NAME}")
    print(f"Device: {DEVICE}")
    print(f"Number of Classes: {NUM_CLASSES}")
    print(f"Classes: {', '.join(CLASS_NAMES)}")
    print(f"\nDataset:")
    print(f"  Train: {TRAIN_DIR}")
    print(f"  Validation: {VAL_DIR}")
    print(f"  Test: {TEST_DIR}")
    print(f"\nHyperparameters:")
    print(f"  Batch Size: {BATCH_SIZE}")
    print(f"  Epochs: {NUM_EPOCHS}")
    print(f"  Learning Rate: {LEARNING_RATE}")
    print(f"  Weight Decay: {WEIGHT_DECAY}")
    print(f"  Image Size: {IMAGE_SIZE}x{IMAGE_SIZE}")
    print(f"\nTraining Settings:")
    print(f"  Early Stopping Patience: {EARLY_STOPPING_PATIENCE}")
    print(f"  Workers: {NUM_WORKERS}")
    print(f"  Random Seed: {RANDOM_SEED}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    print_config()

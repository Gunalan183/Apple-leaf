"""
Quick training script for fast testing
Uses fewer epochs and smaller model for rapid validation
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Override config for quick training
import config
config.NUM_EPOCHS = 5  # Only 5 epochs instead of 50
config.EARLY_STOPPING_PATIENCE = 3  # Stop earlier
config.BATCH_SIZE = 64  # Larger batches for faster training

# Import and run main training
from train import main

if __name__ == '__main__':
    print("=" * 70)
    print("QUICK TRAINING MODE")
    print("=" * 70)
    print("⚡ Configuration:")
    print(f"   Epochs: {config.NUM_EPOCHS} (reduced from 50)")
    print(f"   Batch Size: {config.BATCH_SIZE} (increased from 32)")
    print(f"   Early Stopping: {config.EARLY_STOPPING_PATIENCE} epochs")
    print("=" * 70)
    print()
    
    main()

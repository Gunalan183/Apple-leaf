#!/usr/bin/env python
"""Check augmented model checkpoint status"""

import torch
from pathlib import Path

checkpoint_path = Path(__file__).parent.parent / "checkpoints" / "densenet121_augmented_best.pth"

if checkpoint_path.exists():
    print(f"Loading checkpoint: {checkpoint_path}")
    checkpoint = torch.load(checkpoint_path, map_location='cpu', weights_only=False)
    
    print("=" * 60)
    print("AUGMENTED MODEL CHECKPOINT STATUS")
    print("=" * 60)
    print(f"Epoch: {checkpoint['epoch']}")
    print(f"Validation Loss: {checkpoint['val_loss']:.4f}")
    print(f"Validation Accuracy: {checkpoint['val_acc']:.4f} ({checkpoint['val_acc']*100:.2f}%)")
    print("=" * 60)
else:
    print("No augmented checkpoint found yet")

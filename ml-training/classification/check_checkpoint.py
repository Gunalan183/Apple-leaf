#!/usr/bin/env python
"""Quick script to check training checkpoint status"""

import torch
from pathlib import Path

checkpoint_path = Path(__file__).parent.parent / "checkpoints" / "densenet121_latest.pth"

if checkpoint_path.exists():
    print(f"Loading checkpoint: {checkpoint_path}")
    checkpoint = torch.load(checkpoint_path, map_location='cpu', weights_only=False)
    
    print("\n" + "=" * 60)
    print("CHECKPOINT STATUS")
    print("=" * 60)
    print(f"Epoch: {checkpoint['epoch']}")
    print(f"Validation Loss: {checkpoint['val_loss']:.4f}")
    print(f"Validation Accuracy: {checkpoint['val_acc']:.4f}")
    
    if 'train_loss' in checkpoint:
        print(f"Training Loss: {checkpoint['train_loss']:.4f}")
    if 'train_acc' in checkpoint:
        print(f"Training Accuracy: {checkpoint['train_acc']:.4f}")
    if 'lr' in checkpoint:
        print(f"Learning Rate: {checkpoint['lr']}")
    
    print("=" * 60)
else:
    print("No checkpoint found yet")

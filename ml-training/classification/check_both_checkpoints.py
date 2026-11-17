#!/usr/bin/env python
"""Check both best and latest checkpoints"""

import torch
from pathlib import Path

base_dir = Path(__file__).parent.parent
best_path = base_dir / "checkpoints" / "densenet121_best.pth"
latest_path = base_dir / "checkpoints" / "densenet121_latest.pth"

print("=" * 70)
print("CHECKPOINT COMPARISON")
print("=" * 70)

if best_path.exists():
    print("\nBEST MODEL:")
    best = torch.load(best_path, map_location='cpu', weights_only=False)
    print(f"  Epoch: {best['epoch']}")
    print(f"  Validation Accuracy: {best['val_acc']:.4f} ({best['val_acc']*100:.2f}%)")
    print(f"  Validation Loss: {best['val_loss']:.4f}")
else:
    print("\nBEST MODEL: Not found")

if latest_path.exists():
    print("\nLATEST MODEL:")
    latest = torch.load(latest_path, map_location='cpu', weights_only=False)
    print(f"  Epoch: {latest['epoch']}")
    print(f"  Validation Accuracy: {latest['val_acc']:.4f} ({latest['val_acc']*100:.2f}%)")
    print(f"  Validation Loss: {latest['val_loss']:.4f}")
else:
    print("\nLATEST MODEL: Not found")

print("\n" + "=" * 70)
print("RECOMMENDATION")
print("=" * 70)

if best_path.exists() and latest_path.exists():
    if best['val_acc'] >= latest['val_acc']:
        print("✅ Best model has highest accuracy - ready for evaluation!")
    else:
        print("ℹ️  Latest model has higher accuracy than 'best' checkpoint")
        print("   (This can happen if training was interrupted)")
    
    if best['val_acc'] >= 0.85:
        print(f"✅ Validation accuracy ({best['val_acc']*100:.2f}%) exceeds target (85%)")
        print("\nReady to proceed with:")
        print("  1. python evaluate.py    # Test set evaluation")
        print("  2. python visualize.py   # Training curves (if history exists)")
        print("  3. python gradcam.py     # Explainability")

print("=" * 70)

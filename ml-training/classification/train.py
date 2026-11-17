"""
GAN-Sim-GAN Training Script
Train DenseNet121 classifier on Apple Leaf Disease dataset
"""

import os
import sys
import gc

# Fix Windows encoding issue
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Force garbage collection before heavy imports
gc.collect()

import torch
torch.set_num_threads(2)  # Limit PyTorch CPU threads to reduce memory
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import ReduceLROnPlateau
import time
import copy
import json
import random
import numpy as np
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from classification.config import *
from classification.dataset import create_dataloaders
from classification.transforms import get_transforms
from classification.model import create_model, save_checkpoint, print_model_summary


def set_seed(seed=42):
    """Set random seeds for reproducibility"""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def train_one_epoch(model, train_loader, criterion, optimizer, device, epoch):
    """
    Train for one epoch
    
    Returns:
        tuple: (average_loss, accuracy)
    """
    model.train()
    running_loss = 0.0
    running_corrects = 0
    total_samples = 0
    
    for batch_idx, (inputs, labels) in enumerate(train_loader):
        inputs = inputs.to(device)
        labels = labels.to(device)
        
        # Zero the parameter gradients
        optimizer.zero_grad()
        
        # Forward pass
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        _, preds = torch.max(outputs, 1)
        
        # Backward pass and optimize
        loss.backward()
        optimizer.step()
        
        # Statistics
        running_loss += loss.item() * inputs.size(0)
        running_corrects += torch.sum(preds == labels.data)
        total_samples += inputs.size(0)
        
        # Print progress every 10 batches
        if (batch_idx + 1) % 10 == 0:
            batch_loss = running_loss / total_samples
            batch_acc = running_corrects.double() / total_samples
            print(f'   Batch [{batch_idx + 1}/{len(train_loader)}] '
                  f'Loss: {batch_loss:.4f} Acc: {batch_acc:.4f}')
    
    epoch_loss = running_loss / total_samples
    epoch_acc = running_corrects.double() / total_samples
    
    return epoch_loss, epoch_acc.item()


def validate(model, val_loader, criterion, device):
    """
    Validate model
    
    Returns:
        tuple: (average_loss, accuracy)
    """
    model.eval()
    running_loss = 0.0
    running_corrects = 0
    total_samples = 0
    
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            
            # Forward pass
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            _, preds = torch.max(outputs, 1)
            
            # Statistics
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)
            total_samples += inputs.size(0)
    
    epoch_loss = running_loss / total_samples
    epoch_acc = running_corrects.double() / total_samples
    
    return epoch_loss, epoch_acc.item()


def train_model(model, train_loader, val_loader, criterion, optimizer, 
                scheduler, device, num_epochs=50, early_stopping_patience=10):
    """
    Train model with early stopping
    
    Returns:
        tuple: (best_model, history)
    """
    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0
    best_loss = float('inf')
    epochs_no_improve = 0
    
    history = {
        'train_loss': [],
        'train_acc': [],
        'val_loss': [],
        'val_acc': [],
        'lr': []
    }
    
    start_time = time.time()
    
    for epoch in range(num_epochs):
        epoch_start = time.time()
        current_lr = optimizer.param_groups[0]['lr']
        
        print(f'\nEpoch {epoch + 1}/{num_epochs}')
        print(f'Learning Rate: {current_lr:.6f}')
        print('-' * 70)
        
        # Training phase
        print('🔵 Training...')
        train_loss, train_acc = train_one_epoch(
            model, train_loader, criterion, optimizer, device, epoch
        )
        
        # Validation phase
        print('🟢 Validating...')
        val_loss, val_acc = validate(model, val_loader, criterion, device)
        
        # Learning rate scheduling
        scheduler.step(val_loss)
        
        # Update history
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)
        history['lr'].append(current_lr)
        
        epoch_time = time.time() - epoch_start
        
        print(f'\n📊 Epoch {epoch + 1} Summary:')
        print(f'   Train Loss: {train_loss:.4f}  Train Acc: {train_acc:.4f}')
        print(f'   Val Loss:   {val_loss:.4f}  Val Acc:   {val_acc:.4f}')
        print(f'   Time: {epoch_time:.2f}s')
        
        # Save latest checkpoint
        save_checkpoint(model, optimizer, epoch + 1, val_loss, val_acc, CHECKPOINT_LATEST)
        
        # Check if this is the best model
        if val_acc > best_acc:
            print(f'   🎉 New best accuracy: {val_acc:.4f} (previous: {best_acc:.4f})')
            best_acc = val_acc
            best_loss = val_loss
            best_model_wts = copy.deepcopy(model.state_dict())
            epochs_no_improve = 0
            
            # Save best checkpoint
            save_checkpoint(model, optimizer, epoch + 1, val_loss, val_acc, CHECKPOINT_BEST)
        else:
            epochs_no_improve += 1
            print(f'   No improvement for {epochs_no_improve} epoch(s)')
        
        # Early stopping check
        if epochs_no_improve >= early_stopping_patience:
            print(f'\n⚠️  Early stopping triggered after {epoch + 1} epochs')
            print(f'   Best validation accuracy: {best_acc:.4f}')
            break
    
    total_time = time.time() - start_time
    
    print('\n' + '=' * 70)
    print('TRAINING COMPLETED!')
    print('=' * 70)
    print(f'Total training time: {total_time / 60:.2f} minutes')
    print(f'Best validation accuracy: {best_acc:.4f}')
    print(f'Best validation loss: {best_loss:.4f}')
    print('=' * 70)
    
    # Load best model weights
    model.load_state_dict(best_model_wts)
    
    return model, history


def save_training_history(history, filepath):
    """Save training history to JSON file"""
    with open(filepath, 'w') as f:
        json.dump(history, f, indent=2)
    print(f'\n💾 Training history saved: {filepath}')


def main():
    """Main training function"""
    print("=" * 70)
    print("GAN-SIM-GAN: TRAINING DENSENET121 CLASSIFIER")
    print("=" * 70)
    
    # Set random seed
    set_seed(RANDOM_SEED)
    print(f"\n🎲 Random seed set to: {RANDOM_SEED}")
    
    # Print configuration
    print_config()
    
    # Check device
    print(f"💻 Using device: {DEVICE}")
    if DEVICE.type == 'cuda':
        print(f"   GPU: {torch.cuda.get_device_name(0)}")
        print(f"   Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
    
    # Create data transforms
    print("\n📊 Creating data transforms...")
    train_transform, val_transform = get_transforms()
    
    # Create dataloaders
    print("\n📦 Loading datasets...")
    train_loader, val_loader, test_loader, dataset_sizes, class_names = create_dataloaders(
        train_dir=TRAIN_DIR,
        val_dir=VAL_DIR,
        test_dir=TEST_DIR,
        train_transform=train_transform,
        val_transform=val_transform,
        batch_size=BATCH_SIZE,
        num_workers=NUM_WORKERS,
        class_names=CLASS_NAMES
    )
    
    # Create model
    print("\n🔨 Creating model...")
    model = create_model(MODEL_NAME, NUM_CLASSES, PRETRAINED)
    model = model.to(DEVICE)
    print_model_summary(model)
    
    # Define loss function
    criterion = nn.CrossEntropyLoss()
    
    # Define optimizer
    optimizer = optim.Adam(
        model.parameters(),
        lr=LEARNING_RATE,
        weight_decay=WEIGHT_DECAY
    )
    
    # Define learning rate scheduler
    scheduler = ReduceLROnPlateau(
        optimizer,
        mode=LR_SCHEDULER['mode'],
        factor=LR_SCHEDULER['factor'],
        patience=LR_SCHEDULER['patience'],
        min_lr=LR_SCHEDULER['min_lr']
    )
    
    print(f"\n⚙️  Training Configuration:")
    print(f"   Loss Function: {criterion.__class__.__name__}")
    print(f"   Optimizer: {optimizer.__class__.__name__}")
    print(f"   Learning Rate: {LEARNING_RATE}")
    print(f"   Weight Decay: {WEIGHT_DECAY}")
    print(f"   Scheduler: {scheduler.__class__.__name__}")
    print(f"   Batch Size: {BATCH_SIZE}")
    print(f"   Epochs: {NUM_EPOCHS}")
    print(f"   Early Stopping Patience: {EARLY_STOPPING_PATIENCE}")
    
    # Train model
    print("\n🚀 Starting training...")
    print("=" * 70)
    
    best_model, history = train_model(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        criterion=criterion,
        optimizer=optimizer,
        scheduler=scheduler,
        device=DEVICE,
        num_epochs=NUM_EPOCHS,
        early_stopping_patience=EARLY_STOPPING_PATIENCE
    )
    
    # Save training history
    save_training_history(history, TRAINING_HISTORY)
    
    print("\n✅ Training pipeline completed successfully!")
    print(f"\n📁 Outputs:")
    print(f"   Best model: {CHECKPOINT_BEST}")
    print(f"   Latest model: {CHECKPOINT_LATEST}")
    print(f"   Training history: {TRAINING_HISTORY}")
    print(f"\n🎯 Next step: Run 'python evaluate.py' to test the model")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Training interrupted by user")
        print("   Progress has been saved in latest checkpoint")
    except Exception as e:
        print(f"\n\n❌ Training failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

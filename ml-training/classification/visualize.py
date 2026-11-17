"""
GAN-Sim-GAN Training Visualization
Visualize training history and generate plots
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from classification.config import TRAINING_HISTORY, REPORTS_DIR


def load_training_history(filepath):
    """Load training history from JSON file"""
    if not filepath.exists():
        raise FileNotFoundError(f"Training history not found at {filepath}")
    
    with open(filepath, 'r') as f:
        history = json.load(f)
    
    return history


def plot_training_curves(history, save_path):
    """
    Plot training and validation loss/accuracy curves
    
    Args:
        history: Training history dictionary
        save_path: Path to save plot
    """
    epochs = range(1, len(history['train_loss']) + 1)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Loss plot
    ax1.plot(epochs, history['train_loss'], 'b-', label='Training Loss', linewidth=2)
    ax1.plot(epochs, history['val_loss'], 'r-', label='Validation Loss', linewidth=2)
    ax1.set_title('Model Loss', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Epoch', fontsize=12)
    ax1.set_ylabel('Loss', fontsize=12)
    ax1.legend(loc='upper right', fontsize=10)
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # Find best epoch
    best_epoch = np.argmin(history['val_loss']) + 1
    best_val_loss = min(history['val_loss'])
    ax1.axvline(x=best_epoch, color='g', linestyle='--', alpha=0.7, label=f'Best (Epoch {best_epoch})')
    ax1.plot(best_epoch, best_val_loss, 'go', markersize=10)
    
    # Accuracy plot
    ax2.plot(epochs, history['train_acc'], 'b-', label='Training Accuracy', linewidth=2)
    ax2.plot(epochs, history['val_acc'], 'r-', label='Validation Accuracy', linewidth=2)
    ax2.set_title('Model Accuracy', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Epoch', fontsize=12)
    ax2.set_ylabel('Accuracy', fontsize=12)
    ax2.legend(loc='lower right', fontsize=10)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.set_ylim([0, 1])
    
    # Find best epoch
    best_epoch_acc = np.argmax(history['val_acc']) + 1
    best_val_acc = max(history['val_acc'])
    ax2.axvline(x=best_epoch_acc, color='g', linestyle='--', alpha=0.7, label=f'Best (Epoch {best_epoch_acc})')
    ax2.plot(best_epoch_acc, best_val_acc, 'go', markersize=10)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✓ Training curves saved: {save_path}")


def plot_learning_rate(history, save_path):
    """
    Plot learning rate schedule
    
    Args:
        history: Training history dictionary
        save_path: Path to save plot
    """
    epochs = range(1, len(history['lr']) + 1)
    
    plt.figure(figsize=(10, 5))
    plt.plot(epochs, history['lr'], 'b-', linewidth=2)
    plt.title('Learning Rate Schedule', fontsize=14, fontweight='bold')
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('Learning Rate', fontsize=12)
    plt.yscale('log')
    plt.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✓ Learning rate plot saved: {save_path}")


def plot_overfitting_analysis(history, save_path):
    """
    Plot training vs validation gap to analyze overfitting
    
    Args:
        history: Training history dictionary
        save_path: Path to save plot
    """
    epochs = range(1, len(history['train_loss']) + 1)
    
    # Calculate gaps
    loss_gap = np.array(history['val_loss']) - np.array(history['train_loss'])
    acc_gap = np.array(history['train_acc']) - np.array(history['val_acc'])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Loss gap
    ax1.plot(epochs, loss_gap, 'r-', linewidth=2)
    ax1.axhline(y=0, color='g', linestyle='--', alpha=0.5)
    ax1.fill_between(epochs, 0, loss_gap, where=(loss_gap > 0), 
                     color='red', alpha=0.3, label='Overfitting Region')
    ax1.set_title('Validation-Train Loss Gap', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Epoch', fontsize=12)
    ax1.set_ylabel('Val Loss - Train Loss', fontsize=12)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # Accuracy gap
    ax2.plot(epochs, acc_gap, 'r-', linewidth=2)
    ax2.axhline(y=0, color='g', linestyle='--', alpha=0.5)
    ax2.fill_between(epochs, 0, acc_gap, where=(acc_gap > 0),
                     color='red', alpha=0.3, label='Overfitting Region')
    ax2.set_title('Train-Validation Accuracy Gap', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Epoch', fontsize=12)
    ax2.set_ylabel('Train Acc - Val Acc', fontsize=12)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✓ Overfitting analysis saved: {save_path}")


def plot_combined_dashboard(history, save_path):
    """
    Create comprehensive training dashboard
    
    Args:
        history: Training history dictionary
        save_path: Path to save plot
    """
    epochs = range(1, len(history['train_loss']) + 1)
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # 1. Training curves (loss)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(epochs, history['train_loss'], 'b-', label='Train', linewidth=2)
    ax1.plot(epochs, history['val_loss'], 'r-', label='Validation', linewidth=2)
    ax1.set_title('Loss Curves', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Training curves (accuracy)
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(epochs, history['train_acc'], 'b-', label='Train', linewidth=2)
    ax2.plot(epochs, history['val_acc'], 'r-', label='Validation', linewidth=2)
    ax2.set_title('Accuracy Curves', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim([0, 1])
    
    # 3. Learning rate
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(epochs, history['lr'], 'g-', linewidth=2)
    ax3.set_title('Learning Rate Schedule', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Epoch')
    ax3.set_ylabel('Learning Rate')
    ax3.set_yscale('log')
    ax3.grid(True, alpha=0.3)
    
    # 4. Loss gap
    ax4 = fig.add_subplot(gs[1, 1])
    loss_gap = np.array(history['val_loss']) - np.array(history['train_loss'])
    ax4.plot(epochs, loss_gap, 'r-', linewidth=2)
    ax4.axhline(y=0, color='g', linestyle='--', alpha=0.5)
    ax4.fill_between(epochs, 0, loss_gap, where=(loss_gap > 0), color='red', alpha=0.3)
    ax4.set_title('Loss Gap (Val - Train)', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Epoch')
    ax4.set_ylabel('Gap')
    ax4.grid(True, alpha=0.3)
    
    # 5. Best metrics summary
    ax5 = fig.add_subplot(gs[2, :])
    ax5.axis('off')
    
    # Calculate summary statistics
    best_val_loss = min(history['val_loss'])
    best_val_acc = max(history['val_acc'])
    best_epoch_loss = np.argmin(history['val_loss']) + 1
    best_epoch_acc = np.argmax(history['val_acc']) + 1
    final_train_loss = history['train_loss'][-1]
    final_train_acc = history['train_acc'][-1]
    final_val_loss = history['val_loss'][-1]
    final_val_acc = history['val_acc'][-1]
    
    summary_text = f"""
    TRAINING SUMMARY
    {'='*60}
    
    Best Validation Loss:     {best_val_loss:.4f} (Epoch {best_epoch_loss})
    Best Validation Accuracy: {best_val_acc:.4f} (Epoch {best_epoch_acc})
    
    Final Training Loss:      {final_train_loss:.4f}
    Final Training Accuracy:  {final_train_acc:.4f}
    Final Validation Loss:    {final_val_loss:.4f}
    Final Validation Accuracy: {final_val_acc:.4f}
    
    Total Epochs Trained:     {len(epochs)}
    """
    
    ax5.text(0.5, 0.5, summary_text, 
            transform=ax5.transAxes,
            fontsize=11,
            verticalalignment='center',
            horizontalalignment='center',
            fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.suptitle('Training Dashboard', fontsize=16, fontweight='bold', y=0.98)
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✓ Training dashboard saved: {save_path}")


def print_training_summary(history):
    """Print training summary statistics"""
    print("\n" + "=" * 70)
    print("TRAINING SUMMARY")
    print("=" * 70)
    
    # Best metrics
    best_val_loss = min(history['val_loss'])
    best_val_acc = max(history['val_acc'])
    best_epoch_loss = np.argmin(history['val_loss']) + 1
    best_epoch_acc = np.argmax(history['val_acc']) + 1
    
    print(f"\n🏆 Best Performance:")
    print(f"   Validation Loss:     {best_val_loss:.4f} (Epoch {best_epoch_loss})")
    print(f"   Validation Accuracy: {best_val_acc:.4f} (Epoch {best_epoch_acc})")
    
    # Final metrics
    final_train_loss = history['train_loss'][-1]
    final_train_acc = history['train_acc'][-1]
    final_val_loss = history['val_loss'][-1]
    final_val_acc = history['val_acc'][-1]
    
    print(f"\n📊 Final Metrics:")
    print(f"   Training:   Loss={final_train_loss:.4f}, Acc={final_train_acc:.4f}")
    print(f"   Validation: Loss={final_val_loss:.4f}, Acc={final_val_acc:.4f}")
    
    # Training progress
    print(f"\n⏱️  Training Progress:")
    print(f"   Total Epochs: {len(history['train_loss'])}")
    print(f"   Final Learning Rate: {history['lr'][-1]:.6f}")
    
    # Overfitting analysis
    final_loss_gap = final_val_loss - final_train_loss
    final_acc_gap = final_train_acc - final_val_acc
    
    print(f"\n🔍 Overfitting Analysis:")
    print(f"   Loss Gap (Val-Train): {final_loss_gap:+.4f}")
    print(f"   Acc Gap (Train-Val):  {final_acc_gap:+.4f}")
    
    if final_loss_gap > 0.5 or final_acc_gap > 0.1:
        print("   ⚠️  Warning: Model may be overfitting")
    else:
        print("   ✓ Model generalization looks good")
    
    print("\n" + "=" * 70)


def main():
    """Main visualization function"""
    print("=" * 70)
    print("GAN-SIM-GAN: TRAINING VISUALIZATION")
    print("=" * 70)
    
    # Check if history exists
    if not TRAINING_HISTORY.exists():
        print(f"\n❌ Error: Training history not found at {TRAINING_HISTORY}")
        print("   Please train the model first by running: python train.py")
        return
    
    # Load training history
    print(f"\n📂 Loading training history from: {TRAINING_HISTORY}")
    history = load_training_history(TRAINING_HISTORY)
    
    # Print summary
    print_training_summary(history)
    
    # Generate visualizations
    print("\n📊 Generating visualizations...")
    
    # Training curves
    curves_path = REPORTS_DIR / "training_curves.png"
    plot_training_curves(history, curves_path)
    
    # Learning rate
    lr_path = REPORTS_DIR / "learning_rate_schedule.png"
    plot_learning_rate(history, lr_path)
    
    # Overfitting analysis
    overfit_path = REPORTS_DIR / "overfitting_analysis.png"
    plot_overfitting_analysis(history, overfit_path)
    
    # Combined dashboard
    dashboard_path = REPORTS_DIR / "training_dashboard.png"
    plot_combined_dashboard(history, dashboard_path)
    
    print("\n" + "=" * 70)
    print("✅ VISUALIZATION COMPLETED!")
    print("=" * 70)
    print(f"\n📁 Generated files:")
    print(f"   - {curves_path}")
    print(f"   - {lr_path}")
    print(f"   - {overfit_path}")
    print(f"   - {dashboard_path}")
    print("\n🎯 Check the reports/ directory for all visualizations")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n\n❌ Visualization failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

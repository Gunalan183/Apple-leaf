"""
GAN-Sim-GAN Model Evaluation Script
Evaluate trained model on test set and generate metrics
"""

import torch
import torch.nn as nn
import numpy as np
import json
from pathlib import Path
import sys
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
import matplotlib.pyplot as plt
import seaborn as sns

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from classification.config import *
from classification.dataset import create_dataloaders
from classification.transforms import get_transforms
from classification.model import create_model, load_checkpoint


def evaluate_model(model, test_loader, device, class_names):
    """
    Evaluate model on test set
    
    Returns:
        dict: Evaluation metrics and predictions
    """
    model.eval()
    
    all_preds = []
    all_labels = []
    all_probs = []
    
    print("🔍 Evaluating model on test set...")
    
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            
            # Forward pass
            outputs = model(inputs)
            probs = torch.nn.functional.softmax(outputs, dim=1)
            _, preds = torch.max(outputs, 1)
            
            # Store results
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())
    
    # Convert to numpy arrays
    all_preds = np.array(all_preds)
    all_labels = np.array(all_labels)
    all_probs = np.array(all_probs)
    
    # Calculate metrics
    accuracy = accuracy_score(all_labels, all_preds)
    precision = precision_score(all_labels, all_preds, average='weighted')
    recall = recall_score(all_labels, all_preds, average='weighted')
    f1 = f1_score(all_labels, all_preds, average='weighted')
    
    # Per-class metrics
    precision_per_class = precision_score(all_labels, all_preds, average=None)
    recall_per_class = recall_score(all_labels, all_preds, average=None)
    f1_per_class = f1_score(all_labels, all_preds, average=None)
    
    # Confusion matrix
    cm = confusion_matrix(all_labels, all_preds)
    
    # Classification report
    report = classification_report(
        all_labels, all_preds,
        target_names=class_names,
        output_dict=True
    )
    
    results = {
        'overall': {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1)
        },
        'per_class': {},
        'confusion_matrix': cm.tolist(),
        'predictions': all_preds.tolist(),
        'labels': all_labels.tolist(),
        'probabilities': all_probs.tolist()
    }
    
    # Add per-class metrics
    for i, class_name in enumerate(class_names):
        results['per_class'][class_name] = {
            'precision': float(precision_per_class[i]),
            'recall': float(recall_per_class[i]),
            'f1_score': float(f1_per_class[i]),
            'support': int(report[class_name]['support'])
        }
    
    return results


def print_evaluation_results(results, class_names):
    """Print evaluation results in formatted table"""
    print("\n" + "=" * 70)
    print("EVALUATION RESULTS")
    print("=" * 70)
    
    # Overall metrics
    print("\n📊 Overall Metrics:")
    print(f"   Accuracy:  {results['overall']['accuracy']:.4f}")
    print(f"   Precision: {results['overall']['precision']:.4f}")
    print(f"   Recall:    {results['overall']['recall']:.4f}")
    print(f"   F1-Score:  {results['overall']['f1_score']:.4f}")
    
    # Per-class metrics
    print("\n📈 Per-Class Metrics:")
    print(f"   {'Class':<12} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'Support':<10}")
    print("   " + "-" * 60)
    
    for class_name in class_names:
        metrics = results['per_class'][class_name]
        print(f"   {class_name.capitalize():<12} "
              f"{metrics['precision']:<12.4f} "
              f"{metrics['recall']:<12.4f} "
              f"{metrics['f1_score']:<12.4f} "
              f"{metrics['support']:<10}")
    
    print("\n" + "=" * 70)


def plot_confusion_matrix(cm, class_names, save_path):
    """
    Plot and save confusion matrix
    
    Args:
        cm: Confusion matrix array
        class_names: List of class names
        save_path: Path to save plot
    """
    plt.figure(figsize=(10, 8))
    
    # Normalize confusion matrix
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    
    # Create heatmap
    sns.heatmap(
        cm_normalized,
        annot=True,
        fmt='.2f',
        cmap='Blues',
        xticklabels=[c.capitalize() for c in class_names],
        yticklabels=[c.capitalize() for c in class_names],
        cbar_kws={'label': 'Normalized Count'},
        linewidths=0.5,
        linecolor='gray'
    )
    
    plt.title('Confusion Matrix (Normalized)', fontsize=14, fontweight='bold', pad=20)
    plt.ylabel('True Label', fontsize=12, fontweight='bold')
    plt.xlabel('Predicted Label', fontsize=12, fontweight='bold')
    
    # Add counts as text
    for i in range(len(class_names)):
        for j in range(len(class_names)):
            plt.text(j + 0.5, i + 0.7, f'({cm[i, j]})',
                    ha='center', va='center', fontsize=9, color='gray')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✓ Confusion matrix saved: {save_path}")


def plot_per_class_metrics(results, class_names, save_path):
    """
    Plot per-class metrics bar chart
    
    Args:
        results: Evaluation results dictionary
        class_names: List of class names
        save_path: Path to save plot
    """
    metrics_names = ['precision', 'recall', 'f1_score']
    x = np.arange(len(class_names))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    colors = ['#3b82f6', '#22c55e', '#f59e0b']
    
    for i, metric in enumerate(metrics_names):
        values = [results['per_class'][cn][metric] for cn in class_names]
        ax.bar(x + i * width, values, width, 
               label=metric.capitalize().replace('_', '-'),
               color=colors[i], alpha=0.8)
    
    ax.set_xlabel('Disease Class', fontsize=12, fontweight='bold')
    ax.set_ylabel('Score', fontsize=12, fontweight='bold')
    ax.set_title('Per-Class Performance Metrics', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x + width)
    ax.set_xticklabels([c.capitalize() for c in class_names])
    ax.legend(loc='lower right', fontsize=10)
    ax.set_ylim([0, 1.1])
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for i, metric in enumerate(metrics_names):
        values = [results['per_class'][cn][metric] for cn in class_names]
        for j, v in enumerate(values):
            ax.text(j + i * width, v + 0.02, f'{v:.3f}',
                   ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✓ Per-class metrics saved: {save_path}")


def save_evaluation_report(results, class_names, save_path):
    """Save detailed text evaluation report"""
    lines = []
    lines.append("=" * 70)
    lines.append("GAN-SIM-GAN: MODEL EVALUATION REPORT")
    lines.append("=" * 70)
    lines.append("")
    
    # Overall metrics
    lines.append("OVERALL METRICS")
    lines.append("-" * 70)
    lines.append(f"Accuracy:  {results['overall']['accuracy']:.4f}")
    lines.append(f"Precision: {results['overall']['precision']:.4f}")
    lines.append(f"Recall:    {results['overall']['recall']:.4f}")
    lines.append(f"F1-Score:  {results['overall']['f1_score']:.4f}")
    lines.append("")
    
    # Per-class metrics
    lines.append("PER-CLASS METRICS")
    lines.append("-" * 70)
    
    for class_name in class_names:
        metrics = results['per_class'][class_name]
        lines.append(f"\n{class_name.upper()}:")
        lines.append(f"  Precision: {metrics['precision']:.4f}")
        lines.append(f"  Recall:    {metrics['recall']:.4f}")
        lines.append(f"  F1-Score:  {metrics['f1_score']:.4f}")
        lines.append(f"  Support:   {metrics['support']}")
    
    lines.append("")
    
    # Confusion matrix
    lines.append("CONFUSION MATRIX")
    lines.append("-" * 70)
    cm = np.array(results['confusion_matrix'])
    
    # Header
    header = "         " + "  ".join([f"{c.capitalize():<10}" for c in class_names])
    lines.append(header)
    
    # Rows
    for i, class_name in enumerate(class_names):
        row = f"{class_name.capitalize():<8} "
        row += "  ".join([f"{cm[i, j]:<10}" for j in range(len(class_names))])
        lines.append(row)
    
    lines.append("")
    lines.append("=" * 70)
    lines.append("Report generated successfully!")
    lines.append("=" * 70)
    
    # Save to file
    with open(save_path, 'w') as f:
        f.write('\n'.join(lines))
    
    print(f"   ✓ Text report saved: {save_path}")


def main():
    """Main evaluation function"""
    print("=" * 70)
    print("GAN-SIM-GAN: MODEL EVALUATION")
    print("=" * 70)
    
    # Check if model exists
    if not CHECKPOINT_BEST.exists():
        print(f"\n❌ Error: Model checkpoint not found at {CHECKPOINT_BEST}")
        print("   Please train the model first by running: python train.py")
        return
    
    print(f"\n💻 Using device: {DEVICE}")
    
    # Create data transforms
    print("\n📊 Creating data transforms...")
    _, val_transform = get_transforms()
    
    # Create dataloaders
    print("\n📦 Loading test dataset...")
    _, _, test_loader, dataset_sizes, class_names = create_dataloaders(
        train_dir=TRAIN_DIR,
        val_dir=VAL_DIR,
        test_dir=TEST_DIR,
        train_transform=val_transform,
        val_transform=val_transform,
        batch_size=BATCH_SIZE,
        num_workers=NUM_WORKERS,
        class_names=CLASS_NAMES
    )
    
    print(f"   Test set size: {dataset_sizes['test']} images")
    
    # Load model
    print("\n🔨 Loading trained model...")
    model = create_model(MODEL_NAME, NUM_CLASSES, pretrained=False)
    model, epoch, val_loss, val_acc = load_checkpoint(model, CHECKPOINT_BEST, DEVICE)
    model = model.to(DEVICE)
    
    # Evaluate model
    print("\n" + "=" * 70)
    results = evaluate_model(model, test_loader, DEVICE, class_names)
    
    # Print results
    print_evaluation_results(results, class_names)
    
    # Generate visualizations
    print("\n📊 Generating visualizations...")
    
    cm = np.array(results['confusion_matrix'])
    
    # Confusion matrix
    cm_path = REPORTS_DIR / "confusion_matrix.png"
    plot_confusion_matrix(cm, class_names, cm_path)
    
    # Per-class metrics
    metrics_path = REPORTS_DIR / "per_class_metrics.png"
    plot_per_class_metrics(results, class_names, metrics_path)
    
    # Save evaluation report
    print("\n💾 Saving evaluation results...")
    
    # JSON report
    json_path = REPORTS_DIR / "evaluation_metrics.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"   ✓ JSON report saved: {json_path}")
    
    # Text report
    text_path = REPORTS_DIR / "evaluation_report.txt"
    save_evaluation_report(results, class_names, text_path)
    
    print("\n" + "=" * 70)
    print("✅ EVALUATION COMPLETED!")
    print("=" * 70)
    print(f"\n📁 Generated files:")
    print(f"   - {cm_path}")
    print(f"   - {metrics_path}")
    print(f"   - {json_path}")
    print(f"   - {text_path}")
    print("\n🎯 Next step: Run 'python visualize.py' to visualize training history")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n\n❌ Evaluation failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

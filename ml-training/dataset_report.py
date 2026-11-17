"""
GAN-Sim-GAN Dataset Report Generator
Creates visual report with sample images and statistics
"""

import os
import sys
import json
import random
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PIL import Image
import numpy as np


# Configuration
BASE_DIR = Path(__file__).resolve().parent
DATASETS_DIR = BASE_DIR / "datasets"
APPLE_DIR = DATASETS_DIR / "Apple"
REPORTS_DIR = BASE_DIR / "reports"

CLASS_NAMES = ['scab', 'rust', 'healthy']
RANDOM_SEED = 42


def load_preparation_report():
    """Load the dataset preparation report"""
    report_file = REPORTS_DIR / "dataset_preparation_report.json"
    
    if not report_file.exists():
        print("❌ ERROR: Preparation report not found!")
        print("   Please run 'python prepare_dataset.py' first.")
        return None
    
    with open(report_file, 'r') as f:
        report = json.load(f)
    
    return report


def create_class_distribution_chart(report):
    """Create bar chart showing class distribution across splits"""
    print("\n📊 Creating class distribution chart...")
    
    splits = report['splits']
    
    # Prepare data
    split_names = ['Train', 'Validation', 'Test']
    x = np.arange(len(CLASS_NAMES))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    colors = ['#22c55e', '#3b82f6', '#f59e0b']
    
    for i, (split_key, split_name) in enumerate(zip(['train', 'validation', 'test'], split_names)):
        counts = [splits[split_key].get(class_name, 0) for class_name in CLASS_NAMES]
        ax.bar(x + i * width, counts, width, label=split_name, color=colors[i], alpha=0.8)
    
    ax.set_xlabel('Disease Class', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Images', fontsize=12, fontweight='bold')
    ax.set_title('Dataset Distribution Across Splits', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x + width)
    ax.set_xticklabels([c.capitalize() for c in CLASS_NAMES])
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    chart_path = REPORTS_DIR / "class_distribution_chart.png"
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✓ Saved: {chart_path}")
    return chart_path


def create_split_pie_chart(report):
    """Create pie chart showing split distribution"""
    print("\n🥧 Creating split distribution pie chart...")
    
    summary = report['summary']
    split_counts = summary['by_split']
    
    labels = ['Train', 'Validation', 'Test']
    sizes = [split_counts['train'], split_counts['validation'], split_counts['test']]
    colors = ['#22c55e', '#3b82f6', '#f59e0b']
    explode = (0.05, 0, 0)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    wedges, texts, autotexts = ax.pie(
        sizes,
        explode=explode,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        shadow=True,
        startangle=90,
        textprops={'fontsize': 12, 'fontweight': 'bold'}
    )
    
    # Make percentage text more readable
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(14)
        autotext.set_fontweight('bold')
    
    ax.set_title('Train/Validation/Test Split Distribution', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Add count information
    total = sum(sizes)
    info_text = f"Total Images: {total}\n"
    info_text += f"Train: {split_counts['train']} | Val: {split_counts['validation']} | Test: {split_counts['test']}"
    plt.figtext(0.5, 0.02, info_text, ha='center', fontsize=10, style='italic')
    
    plt.tight_layout()
    chart_path = REPORTS_DIR / "split_distribution_pie.png"
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✓ Saved: {chart_path}")
    return chart_path


def visualize_sample_images(num_samples=3):
    """Create grid of sample images from each class"""
    print(f"\n🖼️  Creating sample image visualization ({num_samples} per class)...")
    
    random.seed(RANDOM_SEED)
    
    # Collect sample images
    samples = {}
    for class_name in CLASS_NAMES:
        class_dir = APPLE_DIR / 'train' / class_name
        if class_dir.exists():
            image_files = list(class_dir.glob('*.[jp][pn][g]*')) + list(class_dir.glob('*.jpeg'))
            if len(image_files) >= num_samples:
                samples[class_name] = random.sample(image_files, num_samples)
            else:
                samples[class_name] = image_files
    
    if not samples:
        print("   ⚠️ No images found for visualization")
        return None
    
    # Create figure
    fig, axes = plt.subplots(len(CLASS_NAMES), num_samples, figsize=(15, 12))
    
    if len(CLASS_NAMES) == 1:
        axes = [axes]
    
    for i, class_name in enumerate(CLASS_NAMES):
        for j in range(num_samples):
            ax = axes[i][j] if num_samples > 1 else axes[i]
            ax.axis('off')
            
            if j < len(samples.get(class_name, [])):
                img_path = samples[class_name][j]
                try:
                    img = Image.open(img_path)
                    # Resize for consistent display
                    img.thumbnail((400, 400), Image.Resampling.LANCZOS)
                    ax.imshow(img)
                    
                    if j == 0:
                        ax.set_title(f"{class_name.capitalize()}", 
                                   fontsize=14, fontweight='bold', loc='left', pad=10)
                except Exception as e:
                    ax.text(0.5, 0.5, f"Error loading\n{img_path.name}", 
                           ha='center', va='center', fontsize=8)
    
    plt.suptitle('Sample Images from Each Disease Class', 
                fontsize=16, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    samples_path = REPORTS_DIR / "sample_images_grid.png"
    plt.savefig(samples_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✓ Saved: {samples_path}")
    return samples_path


def create_detailed_comparison(num_samples=5):
    """Create detailed side-by-side comparison with larger images"""
    print(f"\n🔍 Creating detailed image comparison...")
    
    random.seed(RANDOM_SEED)
    
    fig, axes = plt.subplots(1, len(CLASS_NAMES), figsize=(18, 6))
    
    if len(CLASS_NAMES) == 1:
        axes = [axes]
    
    for i, class_name in enumerate(CLASS_NAMES):
        class_dir = APPLE_DIR / 'train' / class_name
        
        if class_dir.exists():
            image_files = list(class_dir.glob('*.[jp][pn][g]*')) + list(class_dir.glob('*.jpeg'))
            
            if image_files:
                # Pick a good representative image
                sample_img = random.choice(image_files)
                
                try:
                    img = Image.open(sample_img)
                    axes[i].imshow(img)
                    axes[i].set_title(f"{class_name.capitalize()}\n({len(image_files)} images in train set)", 
                                    fontsize=12, fontweight='bold')
                    axes[i].axis('off')
                    
                    # Add filename below
                    axes[i].text(0.5, -0.05, f"{sample_img.name}", 
                               ha='center', transform=axes[i].transAxes, 
                               fontsize=8, style='italic')
                except Exception as e:
                    axes[i].text(0.5, 0.5, f"Error loading image", 
                               ha='center', va='center')
                    axes[i].axis('off')
    
    plt.suptitle('Representative Images from Each Disease Class', 
                fontsize=14, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    comparison_path = REPORTS_DIR / "detailed_comparison.png"
    plt.savefig(comparison_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✓ Saved: {comparison_path}")
    return comparison_path


def generate_text_report(report):
    """Generate detailed text report"""
    print("\n📝 Generating text report...")
    
    text_report = []
    text_report.append("=" * 70)
    text_report.append("GAN-SIM-GAN: APPLE LEAF DISEASE DATASET REPORT")
    text_report.append("=" * 70)
    text_report.append("")
    
    # Dataset Summary
    text_report.append("DATASET SUMMARY")
    text_report.append("-" * 70)
    summary = report['summary']
    text_report.append(f"Total Images: {summary['total_images']}")
    text_report.append(f"Number of Classes: {len(CLASS_NAMES)}")
    text_report.append(f"Classes: {', '.join([c.capitalize() for c in CLASS_NAMES])}")
    text_report.append("")
    
    # Configuration
    text_report.append("CONFIGURATION")
    text_report.append("-" * 70)
    config = report['configuration']
    text_report.append(f"Train Ratio: {config['train_ratio']*100:.0f}%")
    text_report.append(f"Validation Ratio: {config['validation_ratio']*100:.0f}%")
    text_report.append(f"Test Ratio: {config['test_ratio']*100:.0f}%")
    text_report.append(f"Random Seed: {config['random_seed']}")
    text_report.append("")
    
    # Split Distribution
    text_report.append("SPLIT DISTRIBUTION")
    text_report.append("-" * 70)
    splits = report['splits']
    for split in ['train', 'validation', 'test']:
        split_total = sum(splits[split].values())
        split_pct = summary['split_percentages'][split]
        text_report.append(f"\n{split.upper()} SET: {split_total} images ({split_pct:.1f}%)")
        
        for class_name in CLASS_NAMES:
            count = splits[split][class_name]
            class_pct = (count / split_total * 100) if split_total > 0 else 0
            text_report.append(f"  {class_name.capitalize():10s}: {count:4d} images ({class_pct:5.1f}%)")
    
    text_report.append("")
    
    # Class Distribution Across Splits
    text_report.append("CLASS DISTRIBUTION ACROSS ALL SPLITS")
    text_report.append("-" * 70)
    for class_name in CLASS_NAMES:
        total_class = summary['by_class'][class_name]
        class_pct = (total_class / summary['total_images'] * 100)
        text_report.append(f"{class_name.capitalize():10s}: {total_class:4d} images ({class_pct:5.1f}%)")
    
    text_report.append("")
    text_report.append("=" * 70)
    text_report.append("Dataset prepared and ready for training!")
    text_report.append("=" * 70)
    
    # Save to file
    report_path = REPORTS_DIR / "dataset_summary_report.txt"
    with open(report_path, 'w') as f:
        f.write('\n'.join(text_report))
    
    print(f"   ✓ Saved: {report_path}")
    
    # Also print to console
    print("\n" + '\n'.join(text_report))
    
    return report_path


def main():
    """Main execution function"""
    print("=" * 60)
    print("GAN-Sim-GAN: Dataset Report Generator")
    print("=" * 60)
    
    # Create reports directory
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load preparation report
    report = load_preparation_report()
    if report is None:
        sys.exit(1)
    
    # Generate visualizations
    chart1 = create_class_distribution_chart(report)
    chart2 = create_split_pie_chart(report)
    samples = visualize_sample_images(num_samples=3)
    comparison = create_detailed_comparison()
    
    # Generate text report
    text_report = generate_text_report(report)
    
    print("\n" + "=" * 60)
    print("✅ DATASET REPORT COMPLETED!")
    print("=" * 60)
    print("\n📊 Generated files:")
    print(f"   - {REPORTS_DIR / 'class_distribution_chart.png'}")
    print(f"   - {REPORTS_DIR / 'split_distribution_pie.png'}")
    if samples:
        print(f"   - {REPORTS_DIR / 'sample_images_grid.png'}")
    if comparison:
        print(f"   - {REPORTS_DIR / 'detailed_comparison.png'}")
    print(f"   - {REPORTS_DIR / 'dataset_summary_report.txt'}")
    print("\n🎯 Dataset is ready for model training (PHASE 2)!")
    print("=" * 60)


if __name__ == "__main__":
    main()

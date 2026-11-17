"""
GAN-Sim-GAN Dataset Preparation Script
Creates stratified train/validation/test splits (70/15/15)
"""

import os
import sys
import shutil
import random
import json
from pathlib import Path
from PIL import Image
from collections import defaultdict


# Configuration
BASE_DIR = Path(__file__).resolve().parent
DATASETS_DIR = BASE_DIR / "datasets"
APPLE_DIR = DATASETS_DIR / "Apple"
REPORTS_DIR = BASE_DIR / "reports"

# Split ratios
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

# Target classes (normalized names)
CLASS_NAMES = ['scab', 'rust', 'healthy']

# Random seed for reproducibility
RANDOM_SEED = 42


def find_dataset_location():
    """Find the inspection report to get dataset location"""
    report_file = REPORTS_DIR / "dataset_inspection_report.json"
    
    if not report_file.exists():
        print("❌ ERROR: Inspection report not found!")
        print("   Please run 'python inspect_dataset.py' first.")
        return None
    
    with open(report_file, 'r') as f:
        report = json.load(f)
    
    dataset_path = Path(report['dataset_path'])
    classes_info = report['classes']
    
    print(f"✓ Found dataset at: {dataset_path}")
    return dataset_path, classes_info


def create_split_directories():
    """Create train/val/test directory structure"""
    print("\n📁 Creating split directories...")
    
    splits = ['train', 'validation', 'test']
    created_dirs = []
    
    for split in splits:
        split_dir = APPLE_DIR / split
        split_dir.mkdir(parents=True, exist_ok=True)
        
        for class_name in CLASS_NAMES:
            class_dir = split_dir / class_name
            class_dir.mkdir(parents=True, exist_ok=True)
            created_dirs.append(class_dir)
            print(f"   ✓ Created: {class_dir}")
    
    return created_dirs


def collect_valid_images(classes_info):
    """Collect all valid images from each class"""
    print("\n📸 Collecting valid images...")
    
    images_by_class = defaultdict(list)
    
    for class_name, info in classes_info.items():
        class_path = Path(info['path'])
        corrupted_files = set(info.get('corrupted_files', []))
        
        print(f"\n   Processing class: {class_name}")
        
        # Get all image files
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        for img_path in class_path.iterdir():
            if img_path.suffix.lower() in image_extensions:
                # Skip corrupted files
                if img_path.name in corrupted_files:
                    print(f"      ⚠️ Skipping corrupted: {img_path.name}")
                    continue
                
                # Verify image can be opened
                try:
                    with Image.open(img_path) as img:
                        img.verify()
                    images_by_class[class_name].append(img_path)
                except Exception as e:
                    print(f"      ⚠️ Skipping invalid: {img_path.name} ({e})")
        
        print(f"      ✓ Found {len(images_by_class[class_name])} valid images")
    
    return images_by_class


def stratified_split(images_by_class, train_ratio, val_ratio, test_ratio, seed=42):
    """Create stratified split maintaining class proportions"""
    print(f"\n🎲 Creating stratified splits (seed={seed})...")
    print(f"   Train: {train_ratio*100:.0f}%, Val: {val_ratio*100:.0f}%, Test: {test_ratio*100:.0f}%")
    
    random.seed(seed)
    splits = {'train': {}, 'validation': {}, 'test': {}}
    
    for class_name, image_paths in images_by_class.items():
        # Shuffle images
        shuffled = image_paths.copy()
        random.shuffle(shuffled)
        
        total = len(shuffled)
        train_count = int(total * train_ratio)
        val_count = int(total * val_ratio)
        
        # Split indices
        train_end = train_count
        val_end = train_end + val_count
        
        splits['train'][class_name] = shuffled[:train_end]
        splits['validation'][class_name] = shuffled[train_end:val_end]
        splits['test'][class_name] = shuffled[val_end:]
        
        print(f"\n   {class_name.capitalize()}:")
        print(f"      Total: {total}")
        print(f"      Train: {len(splits['train'][class_name])} ({len(splits['train'][class_name])/total*100:.1f}%)")
        print(f"      Val:   {len(splits['validation'][class_name])} ({len(splits['validation'][class_name])/total*100:.1f}%)")
        print(f"      Test:  {len(splits['test'][class_name])} ({len(splits['test'][class_name])/total*100:.1f}%)")
    
    return splits


def copy_images_to_splits(splits):
    """Copy images to their respective split directories"""
    print("\n📋 Copying images to split directories...")
    
    stats = defaultdict(lambda: defaultdict(int))
    
    for split_name, classes in splits.items():
        print(f"\n   Processing {split_name} split...")
        
        for class_name, image_paths in classes.items():
            dest_dir = APPLE_DIR / split_name / class_name
            
            for src_path in image_paths:
                dest_path = dest_dir / src_path.name
                
                try:
                    shutil.copy2(src_path, dest_path)
                    stats[split_name][class_name] += 1
                except Exception as e:
                    print(f"      ⚠️ Failed to copy {src_path.name}: {e}")
            
            print(f"      ✓ Copied {stats[split_name][class_name]} images to {class_name}/")
    
    return stats


def verify_splits():
    """Verify that splits were created correctly"""
    print("\n✓ Verifying splits...")
    
    verification = {}
    
    for split in ['train', 'validation', 'test']:
        split_dir = APPLE_DIR / split
        verification[split] = {}
        
        for class_name in CLASS_NAMES:
            class_dir = split_dir / class_name
            
            if class_dir.exists():
                image_count = len(list(class_dir.glob('*.[jp][pn][g]*')))
                image_count += len(list(class_dir.glob('*.jpeg')))
                verification[split][class_name] = image_count
            else:
                verification[split][class_name] = 0
    
    return verification


def save_preparation_report(splits, verification):
    """Save dataset preparation report"""
    report_file = REPORTS_DIR / "dataset_preparation_report.json"
    
    # Calculate statistics
    total_by_split = {}
    total_by_class = defaultdict(int)
    total_images = 0
    
    for split_name, classes in verification.items():
        total_by_split[split_name] = sum(classes.values())
        total_images += total_by_split[split_name]
        
        for class_name, count in classes.items():
            total_by_class[class_name] += count
    
    report = {
        'configuration': {
            'train_ratio': TRAIN_RATIO,
            'validation_ratio': VAL_RATIO,
            'test_ratio': TEST_RATIO,
            'random_seed': RANDOM_SEED,
            'class_names': CLASS_NAMES
        },
        'splits': verification,
        'summary': {
            'total_images': total_images,
            'by_split': total_by_split,
            'by_class': dict(total_by_class),
            'split_percentages': {
                split: (count / total_images * 100) if total_images > 0 else 0
                for split, count in total_by_split.items()
            }
        },
        'directories': {
            'train': str(APPLE_DIR / 'train'),
            'validation': str(APPLE_DIR / 'validation'),
            'test': str(APPLE_DIR / 'test')
        }
    }
    
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Preparation report saved to: {report_file}")
    return report


def print_summary(verification):
    """Print preparation summary"""
    print("\n" + "=" * 60)
    print("📊 DATASET PREPARATION SUMMARY")
    print("=" * 60)
    
    total_images = sum(sum(classes.values()) for classes in verification.values())
    
    print(f"\n✓ Total Images: {total_images}")
    
    print("\n📈 Split Distribution:")
    for split, classes in verification.items():
        split_total = sum(classes.values())
        percentage = (split_total / total_images * 100) if total_images > 0 else 0
        print(f"\n   {split.capitalize()}: {split_total} images ({percentage:.1f}%)")
        
        for class_name, count in classes.items():
            class_pct = (count / split_total * 100) if split_total > 0 else 0
            print(f"      {class_name.capitalize():10s}: {count:4d} ({class_pct:5.1f}%)")
    
    print("\n📂 Directory Structure:")
    print(f"   {APPLE_DIR}/")
    for split in ['train', 'validation', 'test']:
        print(f"   ├── {split}/")
        for class_name in CLASS_NAMES:
            count = verification[split][class_name]
            print(f"   │   ├── {class_name}/ ({count} images)")
    
    print("\n" + "=" * 60)


def main():
    """Main execution function"""
    print("=" * 60)
    print("GAN-Sim-GAN: Dataset Preparation Tool")
    print("=" * 60)
    
    # Find dataset location from inspection report
    result = find_dataset_location()
    if result is None:
        sys.exit(1)
    
    dataset_path, classes_info = result
    
    # Create split directories
    create_split_directories()
    
    # Collect valid images
    images_by_class = collect_valid_images(classes_info)
    
    if not images_by_class:
        print("\n❌ ERROR: No valid images found!")
        sys.exit(1)
    
    # Create stratified splits
    splits = stratified_split(
        images_by_class,
        TRAIN_RATIO,
        VAL_RATIO,
        TEST_RATIO,
        RANDOM_SEED
    )
    
    # Copy images to split directories
    stats = copy_images_to_splits(splits)
    
    # Verify splits
    verification = verify_splits()
    
    # Save report
    save_preparation_report(splits, verification)
    
    # Print summary
    print_summary(verification)
    
    print("\n✅ DATASET PREPARATION COMPLETED!")
    print("\n📁 Dataset ready for training at:")
    print(f"   {APPLE_DIR}")
    print("\n🎯 Next steps:")
    print("   1. Run 'python dataset_report.py' to generate visual dataset report")
    print("   2. Start model training with PHASE 2")
    print("=" * 60)


if __name__ == "__main__":
    main()

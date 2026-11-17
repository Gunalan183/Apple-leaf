"""
Synthetic Data Generator
Generate augmented training samples using advanced transformations
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from PIL import Image
import argparse
from tqdm import tqdm
import json
import random

try:
    from augmentation.config import *
    from augmentation.advanced_transforms import AugmentationConfig, validate_augmented_image
except ImportError:
    from config import *
    from advanced_transforms import AugmentationConfig, validate_augmented_image


def generate_synthetic_samples(
    original_dir,
    output_dir,
    augmentation_factor=2,
    validate=True,
    max_attempts=10
):
    """
    Generate synthetic augmented samples
    
    Args:
        original_dir: Path to original training dataset
        output_dir: Path to save augmented samples
        augmentation_factor: How many synthetic samples per original image
        validate: Whether to apply quality control
        max_attempts: Maximum attempts to generate valid sample
        
    Returns:
        dict: Generation statistics
    """
    
    print("=" * 70)
    print("SYNTHETIC DATA GENERATION")
    print("=" * 70)
    print(f"Original dataset: {original_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Augmentation factor: {augmentation_factor}x")
    print(f"Quality validation: {'Enabled' if validate else 'Disabled'}")
    print("=" * 70)
    
    # Set random seed
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    
    # Initialize augmentation config
    aug_config = AugmentationConfig()
    
    # Statistics
    stats = {
        'total_original': 0,
        'total_generated': 0,
        'by_class': {},
        'failed_validation': 0,
        'generation_time': 0
    }
    
    # Process each class
    classes = ['scab', 'rust', 'healthy']
    
    for class_name in classes:
        print(f"\n{'=' * 70}")
        print(f"Processing class: {class_name.upper()}")
        print(f"{'=' * 70}")
        
        class_dir = Path(original_dir) / class_name
        output_class_dir = Path(output_dir) / 'train' / class_name
        output_class_dir.mkdir(parents=True, exist_ok=True)
        
        if not class_dir.exists():
            print(f"⚠️  Directory not found: {class_dir}")
            continue
        
        # Get all images
        image_files = list(class_dir.glob('*.jpg')) + list(class_dir.glob('*.png'))
        if not image_files:
            print(f"⚠️  No images found in {class_dir}")
            continue
        
        print(f"Found {len(image_files)} original images")
        
        stats['by_class'][class_name] = {
            'original': len(image_files),
            'generated': 0,
            'failed': 0
        }
        
        # Generate augmented samples
        generated_count = 0
        failed_count = 0
        
        with tqdm(total=len(image_files) * augmentation_factor, desc=f"{class_name}") as pbar:
            for img_path in image_files:
                # Load image
                try:
                    image = np.array(Image.open(img_path).convert('RGB'))
                except Exception as e:
                    print(f"\n❌ Failed to load {img_path.name}: {e}")
                    continue
                
                # Generate multiple augmented versions
                for aug_idx in range(augmentation_factor):
                    attempt = 0
                    success = False
                    
                    while attempt < max_attempts and not success:
                        # Get random intensity augmentation
                        augmentation = aug_config.get_random_intensity()
                        
                        # Apply augmentation
                        augmented = augmentation(image=image)['image']
                        
                        # Validate if enabled
                        if validate:
                            if not validate_augmented_image(augmented):
                                attempt += 1
                                continue
                        
                        # Save augmented image
                        output_name = NAMING_PATTERN.format(
                            class_name=class_name,
                            original=img_path.stem,
                            index=aug_idx
                        )
                        output_path = output_class_dir / output_name
                        
                        try:
                            Image.fromarray(augmented).save(
                                output_path,
                                quality=SAVE_QUALITY,
                                optimize=True
                            )
                            generated_count += 1
                            success = True
                        except Exception as e:
                            print(f"\n❌ Failed to save {output_name}: {e}")
                            attempt += 1
                    
                    if not success:
                        failed_count += 1
                    
                    pbar.update(1)
        
        stats['by_class'][class_name]['generated'] = generated_count
        stats['by_class'][class_name]['failed'] = failed_count
        stats['total_generated'] += generated_count
        stats['failed_validation'] += failed_count
        
        print(f"✅ Generated: {generated_count} images")
        print(f"❌ Failed: {failed_count} images")
    
    # Calculate totals
    stats['total_original'] = sum(s['original'] for s in stats['by_class'].values())
    
    return stats


def copy_validation_test_sets(original_dir, output_dir):
    """
    Copy validation and test sets unchanged
    
    Args:
        original_dir: Path to original dataset
        output_dir: Path to output dataset
    """
    import shutil
    
    print(f"\n{'=' * 70}")
    print("COPYING VALIDATION AND TEST SETS")
    print(f"{'=' * 70}")
    
    for split in ['validation', 'test']:
        src_split = Path(original_dir) / split
        dst_split = Path(output_dir) / split
        
        if not src_split.exists():
            print(f"⚠️  {split} directory not found")
            continue
        
        print(f"\nCopying {split} set...")
        
        for class_name in ['scab', 'rust', 'healthy']:
            src_class = src_split / class_name
            dst_class = dst_split / class_name
            
            if not src_class.exists():
                continue
            
            dst_class.mkdir(parents=True, exist_ok=True)
            
            # Copy all images
            images = list(src_class.glob('*.jpg')) + list(src_class.glob('*.png'))
            for img_path in tqdm(images, desc=f"  {class_name}"):
                shutil.copy2(img_path, dst_class / img_path.name)
        
        print(f"✅ {split.capitalize()} set copied")


def save_generation_report(stats, output_dir):
    """
    Save generation statistics report
    
    Args:
        stats: Generation statistics dict
        output_dir: Output directory
    """
    report_path = REPORTS_DIR / 'synthetic_generation_report.json'
    
    with open(report_path, 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\n📊 Report saved: {report_path}")
    
    # Print summary
    print(f"\n{'=' * 70}")
    print("GENERATION SUMMARY")
    print(f"{'=' * 70}")
    print(f"Total original images: {stats['total_original']}")
    print(f"Total generated images: {stats['total_generated']}")
    print(f"Failed validations: {stats['failed_validation']}")
    print(f"\nPer-class breakdown:")
    for class_name, class_stats in stats['by_class'].items():
        print(f"  {class_name.capitalize()}:")
        print(f"    Original: {class_stats['original']}")
        print(f"    Generated: {class_stats['generated']}")
        print(f"    Failed: {class_stats['failed']}")
        expansion = class_stats['generated'] / class_stats['original'] if class_stats['original'] > 0 else 0
        print(f"    Expansion: {expansion:.1f}x")


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(description='Generate synthetic augmented data')
    parser.add_argument('--factor', type=int, default=AUGMENTATION_FACTOR,
                       help='Augmentation factor (default: 2)')
    parser.add_argument('--output', type=str, default=str(AUGMENTED_DATASET),
                       help='Output directory')
    parser.add_argument('--no-validate', action='store_true',
                       help='Disable quality validation')
    parser.add_argument('--train-only', action='store_true',
                       help='Only generate training data (skip val/test copy)')
    
    args = parser.parse_args()
    
    original_train = ORIGINAL_DATASET / 'train'
    output_dir = Path(args.output)
    
    if not original_train.exists():
        print(f"❌ Error: Training directory not found: {original_train}")
        return
    
    # Generate synthetic training data
    stats = generate_synthetic_samples(
        original_dir=original_train,
        output_dir=output_dir,
        augmentation_factor=args.factor,
        validate=not args.no_validate,
        max_attempts=10
    )
    
    # Copy validation and test sets
    if not args.train_only:
        copy_validation_test_sets(ORIGINAL_DATASET, output_dir)
    
    # Save report
    save_generation_report(stats, output_dir)
    
    print(f"\n{'=' * 70}")
    print("✅ SYNTHETIC DATA GENERATION COMPLETED!")
    print(f"{'=' * 70}")
    print(f"Output directory: {output_dir}")
    print(f"Ready for training with augmented dataset!")
    print(f"{'=' * 70}\n")


if __name__ == '__main__':
    main()

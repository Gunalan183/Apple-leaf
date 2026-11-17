"""
GAN-Sim-GAN Dataset Inspection Script
Inspects the downloaded Apple Leaf Disease dataset structure
"""

import os
import sys
from pathlib import Path
from PIL import Image
import json
from collections import defaultdict


# Configuration
BASE_DIR = Path(__file__).resolve().parent
DATASETS_DIR = BASE_DIR / "datasets"
APPLE_DIR = DATASETS_DIR / "Apple"
REPORTS_DIR = BASE_DIR / "reports"


def find_dataset_location():
    """Find where kagglehub downloaded the dataset"""
    print("🔍 Searching for downloaded dataset...")
    
    # Check download_info.txt
    info_file = APPLE_DIR / "download_info.txt"
    if info_file.exists():
        with open(info_file, 'r') as f:
            for line in f:
                if line.startswith("Download Location:"):
                    path = line.split(":", 1)[1].strip()
                    dataset_path = Path(path)
                    if dataset_path.exists():
                        print(f"   ✓ Found dataset at: {dataset_path}")
                        return dataset_path
    
    # Check common kagglehub cache locations
    possible_locations = [
        Path.home() / ".cache" / "kagglehub" / "datasets" / "nirmalsankalana" / "apple-leaf-disease-dataset",
        Path(os.getenv("USERPROFILE", "")) / ".cache" / "kagglehub" / "datasets" / "nirmalsankalana" / "apple-leaf-disease-dataset",
    ]
    
    for location in possible_locations:
        if location.exists():
            print(f"   ✓ Found dataset at: {location}")
            return location
    
    print("\n❌ ERROR: Could not find downloaded dataset!")
    print("   Please run 'python download_dataset.py' first.")
    return None


def explore_directory_structure(root_path, max_depth=4):
    """Explore and display directory structure"""
    print(f"\n📂 Dataset Directory Structure:")
    print("=" * 60)
    
    structure = {}
    
    def explore(path, depth=0, prefix=""):
        if depth > max_depth:
            return
        
        try:
            items = sorted(path.iterdir())
            dirs = [item for item in items if item.is_dir()]
            files = [item for item in items if item.is_file()]
            
            # Print directories
            for i, dir_item in enumerate(dirs):
                is_last = (i == len(dirs) - 1) and len(files) == 0
                connector = "└── " if is_last else "├── "
                print(f"{prefix}{connector}{dir_item.name}/")
                
                # Record structure
                if depth == 0:
                    structure[dir_item.name] = {"type": "directory", "path": str(dir_item)}
                
                # Recurse
                extension = "    " if is_last else "│   "
                explore(dir_item, depth + 1, prefix + extension)
            
            # Print files (show first few)
            if files:
                shown_files = files[:5]
                for i, file_item in enumerate(shown_files):
                    is_last = (i == len(shown_files) - 1) and len(files) <= 5
                    connector = "└── " if is_last else "├── "
                    print(f"{prefix}{connector}{file_item.name}")
                
                if len(files) > 5:
                    print(f"{prefix}    ... and {len(files) - 5} more files")
        
        except PermissionError:
            print(f"{prefix}[Permission Denied]")
    
    explore(root_path)
    print("=" * 60)
    return structure


def identify_class_directories(root_path):
    """Identify directories containing image classes"""
    print("\n🔎 Identifying disease class directories...")
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    class_dirs = {}
    
    # Search for directories containing images
    for root, dirs, files in os.walk(root_path):
        image_files = [f for f in files if Path(f).suffix.lower() in image_extensions]
        
        if image_files:
            dir_path = Path(root)
            dir_name = dir_path.name.lower()
            
            # Normalize class names
            normalized_name = dir_name
            if 'scab' in dir_name or 'scrab' in dir_name:  # Handle potential misspelling
                normalized_name = 'scab'
            elif 'rust' in dir_name:
                normalized_name = 'rust'
            elif 'healthy' in dir_name:
                normalized_name = 'healthy'
            
            if normalized_name in ['scab', 'rust', 'healthy']:
                class_dirs[normalized_name] = {
                    'path': dir_path,
                    'original_name': dir_name,
                    'image_count': len(image_files),
                    'images': image_files
                }
    
    return class_dirs


def analyze_images(class_dirs):
    """Analyze images in each class directory"""
    print("\n📊 Analyzing images in each class...")
    print("=" * 60)
    
    analysis = {}
    total_images = 0
    
    for class_name, info in class_dirs.items():
        print(f"\n🍎 Class: {class_name.upper()}")
        print(f"   Directory: {info['path']}")
        print(f"   Original name: {info['original_name']}")
        print(f"   Total images: {info['image_count']}")
        
        # Analyze image properties
        valid_images = 0
        corrupted_images = []
        dimensions = []
        formats = defaultdict(int)
        file_sizes = []
        
        for img_name in info['images']:
            img_path = info['path'] / img_name
            
            try:
                # Check file size
                file_size = img_path.stat().st_size
                file_sizes.append(file_size)
                
                # Try to open image
                with Image.open(img_path) as img:
                    valid_images += 1
                    dimensions.append(img.size)
                    formats[img.format] += 1
            
            except Exception as e:
                corrupted_images.append((img_name, str(e)))
        
        # Calculate statistics
        if dimensions:
            widths = [d[0] for d in dimensions]
            heights = [d[1] for d in dimensions]
            avg_width = sum(widths) / len(widths)
            avg_height = sum(heights) / len(heights)
            min_width, max_width = min(widths), max(widths)
            min_height, max_height = min(heights), max(heights)
        else:
            avg_width = avg_height = min_width = max_width = min_height = max_height = 0
        
        avg_size_mb = (sum(file_sizes) / len(file_sizes)) / (1024 * 1024) if file_sizes else 0
        
        print(f"   Valid images: {valid_images}")
        print(f"   Corrupted: {len(corrupted_images)}")
        print(f"   Formats: {dict(formats)}")
        print(f"   Dimensions (avg): {avg_width:.0f} x {avg_height:.0f}")
        print(f"   Dimensions (range): {min_width}-{max_width} x {min_height}-{max_height}")
        print(f"   Average file size: {avg_size_mb:.2f} MB")
        
        if corrupted_images:
            print(f"   ⚠️ Corrupted files:")
            for img_name, error in corrupted_images[:3]:
                print(f"      - {img_name}: {error}")
            if len(corrupted_images) > 3:
                print(f"      ... and {len(corrupted_images) - 3} more")
        
        analysis[class_name] = {
            'path': str(info['path']),
            'original_name': info['original_name'],
            'total_count': info['image_count'],
            'valid_count': valid_images,
            'corrupted_count': len(corrupted_images),
            'corrupted_files': [img for img, _ in corrupted_images],
            'formats': dict(formats),
            'dimensions': {
                'average': {'width': avg_width, 'height': avg_height},
                'min': {'width': min_width, 'height': min_height},
                'max': {'width': max_width, 'height': max_height}
            },
            'avg_file_size_mb': avg_size_mb
        }
        
        total_images += valid_images
    
    print("\n" + "=" * 60)
    print(f"📈 Total valid images across all classes: {total_images}")
    
    return analysis


def detect_duplicates(class_dirs, sample_size=100):
    """Detect potential duplicate images (basic check)"""
    print("\n🔍 Checking for potential duplicates...")
    print("   (Comparing file sizes and first few bytes)")
    
    file_signatures = {}
    potential_duplicates = []
    
    for class_name, info in class_dirs.items():
        for img_name in info['images'][:sample_size]:  # Sample first N images
            img_path = info['path'] / img_name
            
            try:
                file_size = img_path.stat().st_size
                
                # Read first 1KB as signature
                with open(img_path, 'rb') as f:
                    signature = f.read(1024)
                
                key = (file_size, signature)
                
                if key in file_signatures:
                    potential_duplicates.append({
                        'file1': file_signatures[key],
                        'file2': str(img_path),
                        'size': file_size
                    })
                else:
                    file_signatures[key] = str(img_path)
            
            except Exception:
                pass
    
    if potential_duplicates:
        print(f"   ⚠️ Found {len(potential_duplicates)} potential duplicates (in sample)")
        for dup in potential_duplicates[:3]:
            print(f"      - {Path(dup['file1']).name} ≈ {Path(dup['file2']).name}")
    else:
        print("   ✓ No obvious duplicates found in sample")
    
    return potential_duplicates


def save_inspection_report(analysis, duplicates, root_path):
    """Save detailed inspection report"""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_file = REPORTS_DIR / "dataset_inspection_report.json"
    
    report = {
        'dataset_path': str(root_path),
        'classes': analysis,
        'summary': {
            'total_classes': len(analysis),
            'total_images': sum(c['valid_count'] for c in analysis.values()),
            'class_distribution': {
                class_name: info['valid_count'] 
                for class_name, info in analysis.items()
            },
            'potential_duplicates': len(duplicates)
        },
        'duplicates_sample': duplicates[:10]
    }
    
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Inspection report saved to: {report_file}")
    return report


def print_summary(analysis):
    """Print summary statistics"""
    print("\n" + "=" * 60)
    print("📋 DATASET SUMMARY")
    print("=" * 60)
    
    total_valid = sum(c['valid_count'] for c in analysis.values())
    total_corrupted = sum(c['corrupted_count'] for c in analysis.values())
    
    print(f"\n✓ Total Classes: {len(analysis)}")
    print(f"✓ Total Valid Images: {total_valid}")
    print(f"✓ Total Corrupted Images: {total_corrupted}")
    
    print("\n📊 Class Distribution:")
    for class_name, info in analysis.items():
        percentage = (info['valid_count'] / total_valid * 100) if total_valid > 0 else 0
        print(f"   {class_name.capitalize():10s}: {info['valid_count']:4d} images ({percentage:5.1f}%)")
    
    print("\n" + "=" * 60)


def main():
    """Main execution function"""
    print("=" * 60)
    print("GAN-Sim-GAN: Dataset Inspection Tool")
    print("=" * 60)
    
    # Find dataset location
    dataset_path = find_dataset_location()
    if dataset_path is None:
        sys.exit(1)
    
    # Explore directory structure
    structure = explore_directory_structure(dataset_path)
    
    # Identify class directories
    class_dirs = identify_class_directories(dataset_path)
    
    if not class_dirs:
        print("\n❌ ERROR: No class directories found!")
        print("   Expected directories: scab, rust, healthy")
        sys.exit(1)
    
    print(f"\n✓ Found {len(class_dirs)} class directories:")
    for class_name in class_dirs:
        print(f"   - {class_name}")
    
    # Analyze images
    analysis = analyze_images(class_dirs)
    
    # Check for duplicates
    duplicates = detect_duplicates(class_dirs)
    
    # Save report
    save_inspection_report(analysis, duplicates, dataset_path)
    
    # Print summary
    print_summary(analysis)
    
    print("\n✅ INSPECTION COMPLETED!")
    print("\nNext step: Run 'python prepare_dataset.py' to create train/val/test splits")
    print("=" * 60)


if __name__ == "__main__":
    main()

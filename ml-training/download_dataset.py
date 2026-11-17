"""
GAN-Sim-GAN Dataset Download Script
Downloads the Apple Leaf Disease dataset from Kaggle
"""

import os
import sys
from pathlib import Path
import kagglehub

# Configuration
DATASET_OWNER = "nirmalsankalana"
DATASET_NAME = "apple-leaf-disease-dataset"
DATASET_ID = f"{DATASET_OWNER}/{DATASET_NAME}"

# Directories
BASE_DIR = Path(__file__).resolve().parent
DATASETS_DIR = BASE_DIR / "datasets"
APPLE_DIR = DATASETS_DIR / "Apple"
ORIGINAL_DIR = APPLE_DIR / "original"


def create_directories():
    """Create necessary directories"""
    print("📁 Creating directory structure...")
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)
    APPLE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"   ✓ Created: {DATASETS_DIR}")
    print(f"   ✓ Created: {APPLE_DIR}")


def check_kaggle_credentials():
    """Check if Kaggle credentials are configured"""
    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    
    if not kaggle_json.exists():
        print("\n❌ ERROR: Kaggle credentials not found!")
        print("\n📋 To download the dataset, you need to configure Kaggle API:")
        print("\n1. Go to: https://www.kaggle.com/account")
        print("2. Scroll to 'API' section")
        print("3. Click 'Create New Token'")
        print("4. This downloads kaggle.json")
        print(f"5. Place it at: {kaggle_json.parent}")
        print("   (Create the .kaggle folder if it doesn't exist)")
        print("\n6. On Windows, the file should be at:")
        print(f"   C:\\Users\\{os.getenv('USERNAME')}\\.kaggle\\kaggle.json")
        print("\nAfter setting up, run this script again.")
        return False
    
    print(f"✓ Kaggle credentials found at: {kaggle_json}")
    return True


def download_dataset():
    """Download Apple Leaf Disease dataset from Kaggle"""
    print(f"\n📦 Downloading dataset: {DATASET_ID}")
    print("   This may take several minutes depending on your internet speed...\n")
    
    try:
        # Download dataset using kagglehub
        path = kagglehub.dataset_download(DATASET_ID)
        print(f"\n✓ Dataset downloaded successfully!")
        print(f"   Location: {path}")
        return path
    
    except Exception as e:
        print(f"\n❌ ERROR: Failed to download dataset")
        print(f"   Error message: {str(e)}")
        print("\nPossible issues:")
        print("1. Kaggle credentials not properly configured")
        print("2. Dataset name incorrect")
        print("3. No internet connection")
        print("4. You need to accept dataset terms on Kaggle website")
        print(f"\nVisit: https://www.kaggle.com/datasets/{DATASET_ID}")
        return None


def record_download_info(download_path):
    """Record information about the downloaded dataset"""
    info_file = APPLE_DIR / "download_info.txt"
    
    with open(info_file, 'w') as f:
        f.write("Apple Leaf Disease Dataset\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Dataset ID: {DATASET_ID}\n")
        f.write(f"Dataset Owner: {DATASET_OWNER}\n")
        f.write(f"Dataset Name: {DATASET_NAME}\n")
        f.write(f"Download Location: {download_path}\n")
        f.write(f"Kaggle URL: https://www.kaggle.com/datasets/{DATASET_ID}\n")
        f.write("\n" + "=" * 50 + "\n")
        f.write("Dataset Description:\n")
        f.write("This dataset contains images of apple leaves with diseases:\n")
        f.write("  - Scab (Venturia inaequalis)\n")
        f.write("  - Rust (Gymnosporangium spp.)\n")
        f.write("  - Healthy leaves\n")
    
    print(f"\n✓ Download information saved to: {info_file}")


def main():
    """Main execution function"""
    print("=" * 60)
    print("GAN-Sim-GAN: Apple Leaf Disease Dataset Downloader")
    print("=" * 60)
    
    # Create directories
    create_directories()
    
    # Check Kaggle credentials
    print("\n🔑 Checking Kaggle API credentials...")
    if not check_kaggle_credentials():
        sys.exit(1)
    
    # Download dataset
    download_path = download_dataset()
    
    if download_path is None:
        print("\n❌ Dataset download failed. Please fix the issues and try again.")
        sys.exit(1)
    
    # Record download information
    record_download_info(download_path)
    
    # Success message
    print("\n" + "=" * 60)
    print("✅ DATASET DOWNLOAD COMPLETED!")
    print("=" * 60)
    print(f"\nDataset location: {download_path}")
    print(f"\nNext steps:")
    print("1. Run 'python inspect_dataset.py' to examine the dataset structure")
    print("2. Run 'python prepare_dataset.py' to create train/val/test splits")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()

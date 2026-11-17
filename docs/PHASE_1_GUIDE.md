# PHASE 1: Dataset Download and Preparation Guide

## Overview

This phase downloads the Apple Leaf Disease dataset from Kaggle and prepares it for model training by creating stratified train/validation/test splits.

---

## Prerequisites

### 1. Kaggle Account Setup

You need a Kaggle account and API credentials.

**Step-by-step:**

1. **Create Kaggle Account** (if you don't have one)
   - Go to: https://www.kaggle.com
   - Sign up for free

2. **Generate API Token**
   - Go to: https://www.kaggle.com/account
   - Scroll down to "API" section
   - Click "Create New Token"
   - This downloads `kaggle.json` file

3. **Install Kaggle Credentials**
   ```powershell
   # Create .kaggle directory in your user folder
   mkdir C:\Users\<YourUsername>\.kaggle
   
   # Move the downloaded kaggle.json to this folder
   # Final location should be:
   # C:\Users\<YourUsername>\.kaggle\kaggle.json
   ```

4. **Accept Dataset Terms**
   - Visit: https://www.kaggle.com/datasets/nirmalsankalana/apple-leaf-disease-dataset
   - Click "Download" button (you'll be prompted to accept terms)
   - You don't need to actually download manually - just accept terms

---

## PHASE 1 Scripts

Four Python scripts handle the complete dataset pipeline:

1. **download_dataset.py** - Downloads dataset from Kaggle
2. **inspect_dataset.py** - Analyzes dataset structure and quality
3. **prepare_dataset.py** - Creates train/val/test splits
4. **dataset_report.py** - Generates visual reports

---

## Step-by-Step Execution

### Step 1: Download Dataset

```powershell
# Activate Python environment
.\venv\Scripts\Activate.ps1

# Navigate to ML training directory
cd ml-training

# Run download script
python download_dataset.py
```

**What it does:**
- ✓ Checks for Kaggle credentials
- ✓ Downloads dataset using KaggleHub
- ✓ Records download location
- ✓ Creates download_info.txt

**Expected output:**
```
============================================================
GAN-Sim-GAN: Apple Leaf Disease Downloader
============================================================
📁 Creating directory structure...
   ✓ Created: G:\Apple_Leaf\ml-training\datasets
   ✓ Created: G:\Apple_Leaf\ml-training\datasets\Apple

🔑 Checking Kaggle API credentials...
✓ Kaggle credentials found at: C:\Users\...\kaggle.json

📦 Downloading dataset: nirmalsankalana/apple-leaf-disease-dataset
   This may take several minutes...

✓ Dataset downloaded successfully!
   Location: [path to downloaded dataset]

✅ DATASET DOWNLOAD COMPLETED!
```

**Troubleshooting:**

- **Error: Kaggle credentials not found**
  - Make sure kaggle.json is in `C:\Users\<YourUsername>\.kaggle\`
  - Check file permissions

- **Error: Need to accept terms**
  - Visit the dataset page on Kaggle
  - Click download to accept terms
  - Run script again

---

### Step 2: Inspect Dataset

```powershell
# Run inspection script
python inspect_dataset.py
```

**What it does:**
- ✓ Locates downloaded dataset
- ✓ Explores directory structure
- ✓ Identifies disease class folders
- ✓ Counts images per class
- ✓ Checks image validity
- ✓ Detects corrupted images
- ✓ Checks for potential duplicates
- ✓ Analyzes image dimensions and formats
- ✓ Saves inspection_report.json

**Expected output:**
```
============================================================
GAN-Sim-GAN: Dataset Inspection Tool
============================================================
🔍 Searching for downloaded dataset...
   ✓ Found dataset at: [path]

📂 Dataset Directory Structure:
[shows directory tree]

✓ Found 3 class directories:
   - scab
   - rust
   - healthy

📊 Analyzing images in each class...

🍎 Class: SCAB
   Total images: [number]
   Valid images: [number]
   Formats: {'JPEG': X, 'PNG': Y}
   Dimensions (avg): [width] x [height]

[... similar for rust and healthy ...]

📋 DATASET SUMMARY
Total Classes: 3
Total Valid Images: [number]

Class Distribution:
   Scab      : [num] images ([percent]%)
   Rust      : [num] images ([percent]%)
   Healthy   : [num] images ([percent]%)
```

**Outputs:**
- `reports/dataset_inspection_report.json` - Detailed analysis

---

### Step 3: Prepare Splits

```powershell
# Run preparation script
python prepare_dataset.py
```

**What it does:**
- ✓ Creates train/validation/test directories
- ✓ Collects valid images from each class
- ✓ Creates stratified splits (70% train, 15% val, 15% test)
- ✓ Copies images to split directories
- ✓ Verifies splits
- ✓ Saves preparation_report.json

**Split Configuration:**
- **Train**: 70% of data
- **Validation**: 15% of data
- **Test**: 15% of data
- **Random Seed**: 42 (reproducible)

**Expected output:**
```
============================================================
GAN-Sim-GAN: Dataset Preparation Tool
============================================================
✓ Found dataset at: [path]

📁 Creating split directories...
   ✓ Created: train/scab
   ✓ Created: train/rust
   ✓ Created: train/healthy
   [... similar for validation and test ...]

🎲 Creating stratified splits (seed=42)...
   Train: 70%, Val: 15%, Test: 15%

   Scab:
      Total: [X]
      Train: [Y] (70.0%)
      Val:   [Z] (15.0%)
      Test:  [W] (15.0%)

[... similar for other classes ...]

📋 Copying images to split directories...
   Processing train split...
      ✓ Copied [X] images to scab/
      [... similar for other classes ...]

📊 DATASET PREPARATION SUMMARY
✓ Total Images: [number]

Split Distribution:
   Train: [X] images (70.0%)
   Validation: [Y] images (15.0%)
   Test: [Z] images (15.0%)
```

**Directory Structure Created:**
```
ml-training/datasets/Apple/
├── train/
│   ├── scab/        (X images)
│   ├── rust/        (Y images)
│   └── healthy/     (Z images)
├── validation/
│   ├── scab/        (X images)
│   ├── rust/        (Y images)
│   └── healthy/     (Z images)
└── test/
    ├── scab/        (X images)
    ├── rust/        (Y images)
    └── healthy/     (Z images)
```

**Outputs:**
- `reports/dataset_preparation_report.json` - Split statistics
- Split directories with organized images

---

### Step 4: Generate Visual Report

```powershell
# Run report generator
python dataset_report.py
```

**What it does:**
- ✓ Creates class distribution bar chart
- ✓ Creates split distribution pie chart
- ✓ Generates sample image grid
- ✓ Creates detailed comparison view
- ✓ Generates text summary report

**Expected output:**
```
============================================================
GAN-Sim-GAN: Dataset Report Generator
============================================================

📊 Creating class distribution chart...
   ✓ Saved: reports/class_distribution_chart.png

🥧 Creating split distribution pie chart...
   ✓ Saved: reports/split_distribution_pie.png

🖼️  Creating sample image visualization...
   ✓ Saved: reports/sample_images_grid.png

🔍 Creating detailed image comparison...
   ✓ Saved: reports/detailed_comparison.png

📝 Generating text report...
   ✓ Saved: reports/dataset_summary_report.txt

✅ DATASET REPORT COMPLETED!

📊 Generated files:
   - class_distribution_chart.png
   - split_distribution_pie.png
   - sample_images_grid.png
   - detailed_comparison.png
   - dataset_summary_report.txt
```

**Generated Files:**

1. **class_distribution_chart.png** - Bar chart showing image counts per class across splits
2. **split_distribution_pie.png** - Pie chart showing train/val/test distribution
3. **sample_images_grid.png** - Grid of sample images from each class
4. **detailed_comparison.png** - Side-by-side comparison of representative images
5. **dataset_summary_report.txt** - Detailed text report

---

## Dataset Information

### Classes

**1. Apple Scab** (`scab`)
- Fungal disease caused by *Venturia inaequalis*
- Characteristics: Dark olive-green to black lesions on leaves

**2. Apple Rust** (`rust`)
- Fungal disease caused by *Gymnosporangium* species
- Characteristics: Bright orange-rust colored spots

**3. Healthy** (`healthy`)
- Disease-free apple leaves
- Characteristics: Uniform green color, no lesions

### Dataset Properties

- **Image Format**: Primarily JPEG/PNG
- **Image Dimensions**: Variable (will be resized to 224×224 for training)
- **Color Space**: RGB
- **Source**: Real apple leaf photographs

---

## Verification Checklist

After completing all steps, verify:

✅ **Dataset Downloaded**
- [ ] `datasets/Apple/download_info.txt` exists
- [ ] Inspection report shows valid images

✅ **Splits Created**
- [ ] `datasets/Apple/train/` directory exists with 3 class folders
- [ ] `datasets/Apple/validation/` directory exists with 3 class folders
- [ ] `datasets/Apple/test/` directory exists with 3 class folders
- [ ] All folders contain images

✅ **Reports Generated**
- [ ] `reports/dataset_inspection_report.json` exists
- [ ] `reports/dataset_preparation_report.json` exists
- [ ] `reports/dataset_summary_report.txt` exists
- [ ] Visual charts (.png files) generated

✅ **Data Quality**
- [ ] No corrupted images in splits
- [ ] Class distribution is balanced
- [ ] Split ratios are correct (70/15/15)

---

## Important Notes

### Data Integrity

- **No Data Leakage**: Test images are completely separate from training
- **Stratified Splits**: Class proportions maintained across splits
- **Reproducible**: Random seed ensures same splits every time
- **Original Preserved**: Original downloaded data remains untouched

### Data Augmentation

The splits created here are the **base dataset**. Additional augmentation will be applied during training:

- **Training augmentation** (in PHASE 2):
  - Random horizontal flips
  - Random rotations
  - Random crops
  - Color jittering
  - Brightness/contrast variation

- **Simulation-based augmentation** (in PHASE 3):
  - Synthetic lesion generation
  - Texture variation
  - Color manipulation

- **GAN-based augmentation** (in PHASE 4):
  - CycleGAN synthetic images
  - SCIT-generated images

---

## Common Issues

### Issue: "Kaggle credentials not found"
**Solution:**
1. Download kaggle.json from Kaggle account settings
2. Place in `C:\Users\<YourUsername>\.kaggle\`
3. Ensure folder and file permissions are correct

### Issue: "Need to accept dataset terms"
**Solution:**
1. Visit dataset page on Kaggle
2. Click download button (accept terms)
3. Don't need to complete download
4. Run script again

### Issue: "No images found"
**Solution:**
1. Check dataset downloaded completely
2. Verify directory structure
3. Re-run inspection script

### Issue: "Corrupted images detected"
**Solution:**
- This is normal, preparation script automatically skips them
- Check inspection report for details
- Verify sufficient valid images remain

---

## File Sizes

Expected approximate sizes:
- **Downloaded dataset**: ~200-500 MB (varies)
- **Prepared splits**: Same total size (images copied)
- **Reports**: <10 MB
- **Visual charts**: <2 MB each

---

## Next Phase

After completing PHASE 1:

✅ **Ready for PHASE 2: Baseline Deep Learning Model**

PHASE 2 will:
- Build PyTorch Dataset and DataLoader
- Implement data preprocessing
- Train DenseNet121 classifier
- Evaluate model performance
- Save trained model checkpoints

---

## Quick Reference Commands

```powershell
# Complete PHASE 1 sequence
.\venv\Scripts\Activate.ps1
cd ml-training

python download_dataset.py
python inspect_dataset.py
python prepare_dataset.py
python dataset_report.py
```

---

**PHASE 1 Complete! Ready to train AI models! 🚀**

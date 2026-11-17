# PHASE 1 - Dataset Download and Preparation ⏳

## Completion Status: **READY TO EXECUTE**

Date: November 16, 2026

---

## Overview

PHASE 1 creates the complete dataset pipeline for the Apple Leaf Disease classification project. All scripts have been created and are ready for execution.

---

## Created Files ✅

### Python Scripts (4 files)

1. **`ml-training/download_dataset.py`** ✅
   - Downloads dataset from Kaggle using KaggleHub
   - Checks for Kaggle API credentials
   - Records download information
   - Provides detailed error messages and troubleshooting

2. **`ml-training/inspect_dataset.py`** ✅
   - Explores dataset directory structure
   - Identifies disease class directories
   - Counts and validates images
   - Detects corrupted files
   - Checks for duplicates
   - Analyzes image properties (dimensions, formats, sizes)
   - Saves JSON inspection report

3. **`ml-training/prepare_dataset.py`** ✅
   - Creates train/validation/test directory structure
   - Implements stratified splitting (70/15/15)
   - Maintains class distribution across splits
   - Copies images to split directories
   - Verifies split integrity
   - Saves JSON preparation report

4. **`ml-training/dataset_report.py`** ✅
   - Generates class distribution bar chart
   - Creates split distribution pie chart
   - Visualizes sample images grid
   - Creates detailed comparison view
   - Generates comprehensive text report

### Documentation (1 file)

5. **`docs/PHASE_1_GUIDE.md`** ✅
   - Complete step-by-step guide
   - Kaggle setup instructions
   - Script execution details
   - Troubleshooting section
   - Verification checklist

---

## Script Features

### download_dataset.py

**Key Features:**
- ✅ Automatic Kaggle credentials detection
- ✅ Clear error messages with solutions
- ✅ Dataset metadata recording
- ✅ Progress indicators
- ✅ Beginner-friendly output

**Handles:**
- Missing Kaggle credentials
- Network errors
- Dataset access permissions
- Directory creation

### inspect_dataset.py

**Key Features:**
- ✅ Recursive directory exploration
- ✅ Multi-format image support (JPEG, PNG, BMP, TIFF, WEBP)
- ✅ Class name normalization (handles "scrab" → "scab")
- ✅ Corrupted image detection
- ✅ Duplicate image detection (basic)
- ✅ Comprehensive statistics
- ✅ JSON report export

**Analyzes:**
- Image count per class
- Image formats
- Image dimensions (min, max, average)
- File sizes
- Data quality issues

### prepare_dataset.py

**Key Features:**
- ✅ Stratified splitting
- ✅ Reproducible (fixed random seed)
- ✅ Maintains class proportions
- ✅ Skips corrupted images
- ✅ Verification step
- ✅ Detailed reporting

**Configuration:**
- Train: 70%
- Validation: 15%
- Test: 15%
- Random seed: 42

**Directory Structure Created:**
```
datasets/Apple/
├── train/
│   ├── scab/
│   ├── rust/
│   └── healthy/
├── validation/
│   ├── scab/
│   ├── rust/
│   └── healthy/
└── test/
    ├── scab/
    ├── rust/
    └── healthy/
```

### dataset_report.py

**Key Features:**
- ✅ Multiple visualization types
- ✅ Professional charts (matplotlib)
- ✅ Sample image grids
- ✅ Text summary report
- ✅ High-resolution exports (300 DPI)

**Generates:**
1. Class distribution bar chart
2. Split distribution pie chart
3. Sample images grid (3 per class)
4. Detailed comparison view
5. Comprehensive text report

---

## Dataset Configuration

### Target Dataset

**Kaggle Dataset:**
- **Owner**: nirmalsankalana
- **Name**: apple-leaf-disease-dataset
- **ID**: `nirmalsankalana/apple-leaf-disease-dataset`
- **URL**: https://www.kaggle.com/datasets/nirmalsankalana/apple-leaf-disease-dataset

### Disease Classes

1. **Scab** (Apple Scab)
   - Scientific name: *Venturia inaequalis*
   - Characteristics: Dark lesions

2. **Rust** (Apple Rust)
   - Scientific name: *Gymnosporangium* spp.
   - Characteristics: Orange spots

3. **Healthy**
   - Disease-free leaves
   - Characteristics: Uniform green

### Data Splits

| Split | Percentage | Purpose |
|-------|-----------|---------|
| Train | 70% | Model training |
| Validation | 15% | Hyperparameter tuning |
| Test | 15% | Final evaluation |

**Properties:**
- ✅ Stratified by class
- ✅ Reproducible (seed=42)
- ✅ No data leakage
- ✅ Balanced proportions

---

## Prerequisites Checklist

Before executing PHASE 1:

### Kaggle Setup
- [ ] Kaggle account created
- [ ] API token generated  KGAT_de597d9389d881e9c490a2ebbb217f47
- [ ] `kaggle.json` downloaded
- [ ] File placed in `C:\Users\<Username>\.kaggle\`
- [ ] Dataset terms accepted on Kaggle website

### Environment Setup
- [x] Python 3.14.2 installed ✅
- [x] Virtual environment created ✅
- [x] Dependencies installed ✅
- [x] `ml-training/` directory exists ✅
- [x] Scripts created ✅

---

## Execution Sequence

Follow this order:

```powershell
# Step 0: Activate environment
.\venv\Scripts\Activate.ps1
cd ml-training

# Step 1: Download dataset (requires Kaggle setup)
python download_dataset.py

# Step 2: Inspect dataset structure
python inspect_dataset.py

# Step 3: Create train/val/test splits
python prepare_dataset.py

# Step 4: Generate visual reports
python dataset_report.py
```

**Estimated Time:** 15-30 minutes (depending on internet speed)

---

## Expected Outputs

### Directory Structure

```
ml-training/
├── datasets/
│   └── Apple/
│       ├── download_info.txt
│       ├── train/
│       │   ├── scab/
│       │   ├── rust/
│       │   └── healthy/
│       ├── validation/
│       │   ├── scab/
│       │   ├── rust/
│       │   └── healthy/
│       └── test/
│           ├── scab/
│           ├── rust/
│           └── healthy/
├── reports/
│   ├── dataset_inspection_report.json
│   ├── dataset_preparation_report.json
│   ├── dataset_summary_report.txt
│   ├── class_distribution_chart.png
│   ├── split_distribution_pie.png
│   ├── sample_images_grid.png
│   └── detailed_comparison.png
├── download_dataset.py
├── inspect_dataset.py
├── prepare_dataset.py
└── dataset_report.py
```

### Reports Generated

1. **JSON Reports** (machine-readable):
   - `dataset_inspection_report.json` - Full dataset analysis
   - `dataset_preparation_report.json` - Split statistics

2. **Visual Reports** (charts):
   - `class_distribution_chart.png` - Bar chart
   - `split_distribution_pie.png` - Pie chart
   - `sample_images_grid.png` - Image samples
   - `detailed_comparison.png` - Class comparison

3. **Text Report**:
   - `dataset_summary_report.txt` - Human-readable summary

4. **Metadata**:
   - `download_info.txt` - Dataset source information

---

## Key Features Implemented

### Data Integrity
- ✅ No data leakage between splits
- ✅ Stratified sampling maintains class balance
- ✅ Corrupted images automatically excluded
- ✅ Reproducible splits (fixed seed)

### Quality Assurance
- ✅ Image validation before processing
- ✅ Format compatibility checks
- ✅ Dimension analysis
- ✅ Duplicate detection
- ✅ Verification step after splitting

### User Experience
- ✅ Clear progress indicators
- ✅ Detailed error messages
- ✅ Troubleshooting guidance
- ✅ Comprehensive reporting
- ✅ Visual feedback

### Flexibility
- ✅ Handles various image formats
- ✅ Normalizes class names
- ✅ Adapts to dataset structure
- ✅ Configurable split ratios
- ✅ Adjustable random seed

---

## Script Dependencies

All scripts use only the installed dependencies:

**Required packages:**
- `kagglehub` - Dataset download
- `Pillow (PIL)` - Image processing
- `matplotlib` - Visualization
- `numpy` - Numerical operations
- `json` - Report generation
- `pathlib` - File operations

**All already installed in PHASE 0** ✅

---

## Validation & Testing

### What Gets Validated

1. **Image Integrity:**
   - Can image be opened?
   - Is format supported?
   - Are dimensions valid?

2. **Split Quality:**
   - Are ratios correct?
   - Is class distribution maintained?
   - Are all images copied?

3. **Data Quality:**
   - Are there corrupted files?
   - Are there duplicates?
   - Are dimensions consistent?

### Automatic Checks

Scripts include automatic verification:
- ✅ File existence checks
- ✅ Image loading validation
- ✅ Split ratio verification
- ✅ Count reconciliation

---

## Error Handling

### Graceful Failures

Scripts handle common errors:
- ❌ Missing Kaggle credentials → Clear instructions
- ❌ Network errors → Retry guidance
- ❌ Corrupted images → Skip and report
- ❌ Missing directories → Auto-create
- ❌ Permission errors → Error message

### Informative Messages

All errors include:
- ✅ What went wrong
- ✅ Why it happened
- ✅ How to fix it
- ✅ Next steps

---

## Best Practices Implemented

### Code Quality
- ✅ Clear function names
- ✅ Comprehensive docstrings
- ✅ Meaningful variable names
- ✅ Proper error handling
- ✅ Consistent formatting

### Data Science
- ✅ Reproducible results (fixed seed)
- ✅ Stratified sampling
- ✅ No data leakage
- ✅ Quality checks
- ✅ Comprehensive reporting

### User Experience
- ✅ Progress feedback
- ✅ Clear messages
- ✅ Visual outputs
- ✅ Beginner-friendly
- ✅ Well-documented

---

## Integration with Other Phases

### Outputs Used By:

**PHASE 2 (Baseline Model):**
- `datasets/Apple/train/` - Training data
- `datasets/Apple/validation/` - Validation data
- `datasets/Apple/test/` - Test data

**PHASE 3 (Simulation Augmentation):**
- `datasets/Apple/train/` - Source for synthetic generation

**PHASE 4 (GAN Augmentation):**
- `datasets/Apple/train/` - GAN training data

**PHASE 7 (Backend):**
- Class names
- Dataset statistics
- Model evaluation data

**PHASE 8 (Frontend):**
- Sample images for UI
- Statistics for display

---

## Next Phase Prerequisites

After PHASE 1 completion, verify before PHASE 2:

- [ ] All 3 classes present in train/validation/test
- [ ] Minimum images per class met
- [ ] No critical errors in reports
- [ ] Visual inspection of sample images looks correct
- [ ] Split ratios are approximately correct

---

## Troubleshooting Quick Reference

| Problem | Solution |
|---------|----------|
| No Kaggle credentials | Follow PHASE_1_GUIDE.md setup instructions |
| Dataset not found | Run download_dataset.py first |
| Corrupted images | Scripts automatically skip them |
| Import errors | Check virtual environment activated |
| Permission denied | Run PowerShell as Administrator |

---

## Time Estimates

| Task | Duration |
|------|----------|
| Kaggle setup (first time) | 5-10 min |
| Dataset download | 5-15 min |
| Dataset inspection | 1-3 min |
| Split preparation | 2-5 min |
| Report generation | 1-2 min |
| **Total** | **15-35 min** |

*Times vary based on internet speed and dataset size*

---

## Success Criteria

PHASE 1 is complete when:

✅ **Download:**
- [ ] Dataset downloaded from Kaggle
- [ ] `download_info.txt` created

✅ **Inspection:**
- [ ] All 3 classes identified
- [ ] Image counts recorded
- [ ] Corrupted files detected
- [ ] `dataset_inspection_report.json` created

✅ **Preparation:**
- [ ] Train/validation/test directories created
- [ ] Images copied to splits
- [ ] Ratios verified (70/15/15)
- [ ] `dataset_preparation_report.json` created

✅ **Reporting:**
- [ ] Visual charts generated
- [ ] Sample images visualized
- [ ] Text report created

✅ **Verification:**
- [ ] All files and directories exist
- [ ] No critical errors
- [ ] Data ready for training

---

## Status: READY FOR USER EXECUTION

**What's Done:**
- ✅ All 4 Python scripts created
- ✅ Complete documentation written
- ✅ Error handling implemented
- ✅ Validation checks included
- ✅ User guide provided

**What's Needed:**
- ⏳ User to set up Kaggle credentials
- ⏳ User to execute scripts in sequence
- ⏳ User to verify outputs

---

## Command Summary

```powershell
# Complete PHASE 1 in one go
.\venv\Scripts\Activate.ps1
cd ml-training
python download_dataset.py && `
python inspect_dataset.py && `
python prepare_dataset.py && `
python dataset_report.py
```

---

**PHASE 1 Scripts Ready! Waiting for execution! 🚀**

**Next:** Execute the scripts, then proceed to PHASE 2 (Baseline Model Training)

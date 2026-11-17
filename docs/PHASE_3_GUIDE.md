# PHASE 3: Simulation-Based Data Augmentation

**Objective**: Expand the training dataset using advanced, realistic augmentation techniques to improve model robustness and generalization.

---

## Overview

PHASE 3 implements sophisticated data augmentation beyond the basic transformations used in PHASE 2. The goal is to generate photorealistic synthetic training samples that simulate real-world variations in:
- Lighting conditions
- Leaf deformations and shapes
- Camera angles and perspectives
- Environmental backgrounds
- Disease progression stages

---

## Augmentation Strategy

### 1. **Baseline Augmentation (Already Implemented)**
From PHASE 2:
- Random rotation (±15°)
- Random horizontal flip
- Color jitter (brightness, contrast, saturation, hue)

### 2. **Advanced Augmentation (PHASE 3)**

#### Geometric Transformations
- **Perspective transformation** - Simulate different viewing angles
- **Elastic deformation** - Realistic leaf bending and curling
- **Shear transformation** - Leaf orientation variations
- **Scale variations** - Different leaf sizes and zoom levels

#### Photometric Transformations
- **Advanced lighting** - Shadows, highlights, directional lighting
- **Blur variations** - Motion blur, Gaussian blur (camera focus)
- **Noise injection** - Sensor noise, compression artifacts
- **Weather effects** - Rain drops, moisture, dust

#### Domain-Specific Augmentation
- **Disease intensity variation** - Simulate progression stages
- **Background replacement** - Different environmental contexts
- **Occlusion** - Partial leaf visibility (overlapping leaves)
- **Multi-scale patches** - Different zoom levels of disease spots

---

## Implementation Plan

### Step 1: Create Augmentation Library
**File**: `ml-training/augmentation/advanced_transforms.py`
- Implement advanced transformation functions
- Use Albumentations library for efficiency
- Custom transformations for leaf-specific needs

### Step 2: Synthetic Data Generation
**File**: `ml-training/augmentation/generate_synthetic.py`
- Apply augmentations to training set
- Generate 2-3x more training samples
- Maintain class balance
- Quality control filters

### Step 3: Analysis Tools
**File**: `ml-training/augmentation/analyze_augmentation.py`
- Visualize augmentation effects
- Compare original vs augmented samples
- Validate realism and diversity

### Step 4: Dataset Integration
**File**: `ml-training/augmentation/create_augmented_dataset.py`
- Merge original + synthetic data
- Create new train/val/test splits
- Generate updated dataset reports

---

## Directory Structure

```
ml-training/
├── augmentation/              # NEW: Advanced augmentation
│   ├── __init__.py
│   ├── advanced_transforms.py # Advanced transformation library
│   ├── generate_synthetic.py  # Synthetic data generator
│   ├── analyze_augmentation.py # Visualization tools
│   ├── create_augmented_dataset.py # Dataset merger
│   └── config.py              # Augmentation configuration
├── datasets/
│   ├── Apple/                 # Original dataset
│   └── Apple_Augmented/       # NEW: Augmented dataset
│       ├── train/
│       ├── validation/
│       └── test/
└── reports/
    └── augmentation_analysis/ # NEW: Augmentation reports
```

---

## Augmentation Configuration

### Target Dataset Size
- **Original Training**: 1,210 images
- **Augmentation Factor**: 3x
- **Target Training Size**: 3,630 images total
  - Original: 1,210 (retained)
  - Synthetic: 2,420 (generated)

### Class Distribution
Maintain balanced distribution:
- Scab: 414 → 1,242 images (3x)
- Rust: 435 → 1,305 images (3x)
- Healthy: 361 → 1,083 images (3x)

### Quality Control
- Minimum realism score threshold
- Diversity check (avoid duplicate-looking samples)
- Manual review of sample batches

---

## Success Criteria

### Quantitative
- ✅ Generate 2,420 new training samples
- ✅ Maintain class balance (±5%)
- ✅ Dataset diversity score > 0.8
- ✅ No obvious artifacts or unrealistic samples

### Qualitative
- ✅ Augmented samples look realistic
- ✅ Disease features preserved correctly
- ✅ Natural variation in appearance
- ✅ Expert validation (visual inspection)

---

## Expected Outcomes

1. **Larger Training Set**: 3,630 training images (3x increase)
2. **Improved Robustness**: Model handles more real-world variations
3. **Better Generalization**: Reduced overfitting risk
4. **Baseline for GAN**: Comparison point for PHASE 4 GAN-generated data

---

## Timeline

- **Step 1** (Augmentation Library): 30 minutes
- **Step 2** (Generate Synthetic): 1-2 hours (depending on CPU)
- **Step 3** (Analysis): 30 minutes
- **Step 4** (Dataset Integration): 30 minutes

**Total**: ~3-4 hours

---

## Next Steps After PHASE 3

**PHASE 4**: Train CycleGAN to generate even more realistic diseased leaf samples
**PHASE 5**: Retrain classifier with augmented + GAN-generated data
**PHASE 6**: Compare baseline (95%) vs augmented vs GAN-augmented performance

---

## Getting Started

Run these commands in order:

```powershell
# 1. Create augmentation library
cd g:\Apple_Leaf\ml-training\augmentation
python advanced_transforms.py --test

# 2. Generate synthetic data
python generate_synthetic.py --factor 2 --output ../datasets/Apple_Augmented

# 3. Analyze results
python analyze_augmentation.py --samples 30

# 4. Create merged dataset
python create_augmented_dataset.py
```

---

**Let's start building PHASE 3!** 🚀

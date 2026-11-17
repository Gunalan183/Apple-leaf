# GAN-Sim-GAN: ML Training Directory

This directory contains all machine learning training scripts, datasets, and research components for the GAN-Sim-GAN project.

---

## 📁 Directory Structure

```
ml-training/
├── datasets/           # Dataset storage
│   └── Apple/
│       ├── train/      # Training split (70%)
│       ├── validation/ # Validation split (15%)
│       └── test/       # Test split (15%)
│
├── checkpoints/        # Saved model weights
│   └── *.pth          # PyTorch checkpoints
│
├── reports/            # Training reports and visualizations
│   ├── *.json         # JSON reports
│   ├── *.png          # Charts and graphs
│   └── *.txt          # Text summaries
│
├── classification/     # Classification model training
│   ├── dataset.py     # PyTorch Dataset
│   ├── transforms.py  # Data augmentation
│   ├── model.py       # Model architecture
│   ├── train.py       # Training loop
│   └── evaluate.py    # Model evaluation
│
├── simulation/         # Simulation-based augmentation (PHASE 3)
│   ├── leaf_segmentation.py
│   ├── lesion_generator.py
│   └── simulation_augmentation.py
│
├── cyclegan/          # CycleGAN implementation (PHASE 4)
│   ├── generators.py
│   ├── discriminators.py
│   └── train_cyclegan.py
│
├── scit/              # SCIT architecture (PHASE 4)
│   ├── encoder.py
│   ├── decoder.py
│   └── train_scit.py
│
└── evaluation/        # Model evaluation utilities
    ├── metrics.py
    └── visualization.py
```

---

## 🚀 Quick Start

### PHASE 1: Dataset Preparation

```powershell
# Activate environment
.\venv\Scripts\Activate.ps1
cd ml-training

# Execute PHASE 1 scripts
python download_dataset.py       # Download from Kaggle
python inspect_dataset.py        # Analyze dataset
python prepare_dataset.py        # Create splits
python dataset_report.py         # Generate reports
```

### PHASE 2: Baseline Model Training

```powershell
cd classification
python train.py                  # Train DenseNet121
python evaluate.py               # Evaluate model
```

---

## 📊 Dataset Information

### Apple Leaf Disease Dataset

**Source:** Kaggle - `nirmalsankalana/apple-leaf-disease-dataset`

**Classes:**
1. **Scab** - Apple Scab (Venturia inaequalis)
2. **Rust** - Apple Rust (Gymnosporangium spp.)
3. **Healthy** - Disease-free leaves

**Splits:**
- Training: 70%
- Validation: 15%
- Testing: 15%

**Image Properties:**
- Format: JPEG/PNG
- Target Size: 224×224 (resized during training)
- Color: RGB

---

## 🤖 Models

### Classification Models

**Baseline: DenseNet121**
- Pre-trained on ImageNet
- Fine-tuned for 3 classes
- Input size: 224×224×3
- Output: 3 classes (scab, rust, healthy)

**Optional Comparisons:**
- ResNet18
- VGG11
- ShuffleNetV2

### Generative Models

**CycleGAN:**
- Cross-domain image translation
- Unpaired image-to-image translation
- Used for domain adaptation

**SCIT (Style-Consistent Image Translation):**
- Mask-guided generation
- VGG19 feature extraction
- Style-preserving synthesis

---

## 📈 Training Configuration

### Data Augmentation

**Training Augmentation:**
- Random horizontal flip
- Random rotation (±15°)
- Random crop with resize
- Color jitter (brightness, contrast)
- Normalization (ImageNet stats)

**Validation/Test:**
- Center crop
- Resize to 224×224
- Normalization only

### Hyperparameters

```python
BATCH_SIZE = 32
LEARNING_RATE = 0.001
EPOCHS = 50
OPTIMIZER = Adam
SCHEDULER = ReduceLROnPlateau
EARLY_STOPPING = 10 epochs
```

---

## 🎯 PHASE Breakdown

### ✅ PHASE 1: Dataset Preparation (Current)
- Download dataset
- Inspect and validate
- Create train/val/test splits
- Generate reports

### ⏳ PHASE 2: Baseline Classifier
- Implement PyTorch Dataset
- Train DenseNet121
- Evaluate performance
- Save checkpoints

### ⏳ PHASE 3: Simulation Augmentation
- Leaf segmentation
- Synthetic lesion generation
- Texture manipulation
- Color variation

### ⏳ PHASE 4: GAN Augmentation
- CycleGAN training
- SCIT training
- Synthetic image generation

### ⏳ PHASE 5: Augmented Training
- Train with simulation data
- Train with GAN data
- Compare performance
- Final model selection

---

## 📝 Scripts Reference

### Dataset Management

| Script | Purpose |
|--------|---------|
| `download_dataset.py` | Download from Kaggle |
| `inspect_dataset.py` | Analyze structure and quality |
| `prepare_dataset.py` | Create train/val/test splits |
| `dataset_report.py` | Generate visual reports |

### Model Training (Coming in PHASE 2)

| Script | Purpose |
|--------|---------|
| `classification/train.py` | Train classifier |
| `classification/evaluate.py` | Evaluate model |
| `classification/dataset.py` | PyTorch Dataset |
| `classification/model.py` | Model architecture |

### Augmentation (Coming in PHASE 3+)

| Script | Purpose |
|--------|---------|
| `simulation/simulation_augmentation.py` | Generate synthetic data |
| `cyclegan/train_cyclegan.py` | Train CycleGAN |
| `scit/train_scit.py` | Train SCIT |

---

## 💾 Saved Outputs

### Checkpoints

```
checkpoints/
├── densenet121_best.pth       # Best validation model
├── densenet121_latest.pth     # Latest epoch
└── training_history.json      # Training metrics
```

### Reports

```
reports/
├── dataset_inspection_report.json
├── dataset_preparation_report.json
├── dataset_summary_report.txt
├── class_distribution_chart.png
├── split_distribution_pie.png
├── sample_images_grid.png
├── detailed_comparison.png
├── training_history.png
├── confusion_matrix.png
└── evaluation_metrics.json
```

---

## 🔧 Utilities

### GPU Support

Models automatically use GPU if available:

```python
import torch
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")
```

### Reproducibility

Fixed random seeds for reproducible results:

```python
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
```

---

## 📊 Expected Performance

### Baseline DenseNet121

**Target Metrics:**
- Accuracy: >85%
- Precision: >80% per class
- Recall: >80% per class
- F1-Score: >80% per class

*Actual performance depends on dataset quality and size*

### With Augmentation

**Expected Improvement:**
- +5-10% accuracy
- Better generalization
- Reduced overfitting
- More robust to variations

---

## 🐛 Troubleshooting

### Common Issues

**Out of Memory (OOM):**
```python
# Reduce batch size
BATCH_SIZE = 16  # or 8
```

**Slow Training:**
```python
# Use fewer workers
num_workers = 0  # or 1
```

**CUDA Errors:**
```powershell
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"
```

---

## 📚 Documentation

- **PHASE 1 Guide:** `docs/PHASE_1_GUIDE.md`
- **PHASE 1 Completion:** `docs/PHASE_1_COMPLETION.md`
- **Main README:** `../README.md`

---

## 🎓 Research Background

This implementation is inspired by the IEEE paper:
**"GAN-Sim-GAN: Generative Data Augmentation for Apple Leaf Disease Classification"**

### Key Research Components

1. **DenseNet121 Baseline**
   - Transfer learning from ImageNet
   - Fine-tuning for agriculture domain

2. **Simulation-Based Augmentation**
   - FFT-filtered noise
   - Skeleton-based lesion placement
   - Gaussian smoothing

3. **GAN-Based Augmentation**
   - CycleGAN for domain adaptation
   - SCIT for style-consistent translation

4. **Evaluation**
   - Quantitative metrics
   - Ablation studies
   - Visual inspection

---

## 🤝 Contributing

When adding new models or experiments:

1. Create a new directory (e.g., `custom_model/`)
2. Include training and evaluation scripts
3. Document hyperparameters
4. Save results to `reports/`
5. Update this README

---

## 📝 Notes

- Keep original dataset in `datasets/Apple/original/` (gitignored)
- Save only model checkpoints, not raw images to git
- Use meaningful checkpoint names
- Document all experiments in reports/
- Maintain reproducibility with fixed seeds

---

**Ready to train state-of-the-art AI models for agriculture! 🌿🤖**

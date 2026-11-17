# Classification Module

DenseNet121-based classifier for Apple Leaf Disease detection.

## 📁 Files

### Core Scripts

1. **`config.py`** - Central configuration
   - Hyperparameters
   - Paths
   - Device settings

2. **`dataset.py`** - PyTorch Dataset
   - Custom AppleLeafDataset class
   - DataLoader creation
   - Class distribution analysis

3. **`transforms.py`** - Image preprocessing
   - Training augmentation
   - Validation transforms
   - Inference transforms

4. **`model.py`** - Model architecture
   - DenseNet121 creation
   - Checkpoint saving/loading
   - Model summary utilities

5. **`train.py`** - Training script
   - Training loop
   - Validation
   - Early stopping
   - Checkpoint management

6. **`evaluate.py`** - Model evaluation
   - Test set evaluation
   - Metrics calculation
   - Confusion matrix
   - Per-class performance

7. **`visualize.py`** - Training visualization
   - Loss/accuracy curves
   - Learning rate schedule
   - Overfitting analysis
   - Training dashboard

8. **`gradcam.py`** - Explainability
   - Grad-CAM implementation
   - Heatmap visualization
   - Sample generation

## 🚀 Quick Start

### 1. Train Model

```powershell
cd ml-training/classification
python train.py
```

**Expected output:**
- Best model checkpoint
- Latest model checkpoint
- Training history JSON

**Training time:**
- With GPU: ~30-60 minutes
- With CPU: ~2-4 hours

### 2. Evaluate Model

```powershell
python evaluate.py
```

**Generates:**
- Confusion matrix
- Per-class metrics chart
- Evaluation metrics JSON
- Text report

### 3. Visualize Training

```powershell
python visualize.py
```

**Generates:**
- Training curves
- Learning rate schedule
- Overfitting analysis
- Training dashboard

### 4. Generate Grad-CAM

```powershell
python gradcam.py
```

**Generates:**
- Grad-CAM heatmaps for test samples
- Visual explanations

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Training
BATCH_SIZE = 32
NUM_EPOCHS = 50
LEARNING_RATE = 0.001

# Early stopping
EARLY_STOPPING_PATIENCE = 10

# Data augmentation
AUGMENTATION = {
    'rotation_degrees': 15,
    'horizontal_flip_prob': 0.5,
    'color_jitter': {...}
}
```

## 📊 Expected Performance

**Target Metrics:**
- Accuracy: >85%
- Precision: >80% per class
- Recall: >80% per class
- F1-Score: >80% per class

## 🔧 Troubleshooting

### Out of Memory

Reduce batch size:
```python
BATCH_SIZE = 16  # or 8
```

### Slow Training

Reduce number of workers:
```python
NUM_WORKERS = 2  # or 0
```

### CUDA Errors

Check GPU availability:
```powershell
python -c "import torch; print(torch.cuda.is_available())"
```

## 📝 Notes

- Model automatically uses GPU if available
- Training history saved as JSON
- Best model selected by validation accuracy
- Early stopping prevents overfitting
- All outputs saved to `reports/` directory

## 🎯 Next Steps

After training:
1. Review training curves
2. Check confusion matrix
3. Analyze Grad-CAM visualizations
4. Proceed to PHASE 3 (Simulation Augmentation)

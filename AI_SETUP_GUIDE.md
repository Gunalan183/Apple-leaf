# 🤖 AI IDE Setup Guide - Apple Leaf Disease Classifier

This guide is optimized for AI-powered IDEs (like Cursor, GitHub Copilot, Kiro, etc.) to understand and execute the complete project setup from the GitHub repository.

---

## 📋 Project Overview

**Project Name:** Apple Leaf Disease Classifier  
**Type:** Full-Stack AI Web Application  
**Repository:** https://github.com/Gunalan183/Apple-leaf.git  
**Tech Stack:** Python (FastAPI, PyTorch) + React (Vite, Tailwind CSS)  
**Purpose:** AI-powered disease detection for apple leaves with 95%+ accuracy

---

## 🎯 Quick Start Command Sequence

### For AI IDE Auto-Execution:

```bash
# 1. Clone repository
git clone https://github.com/Gunalan183/Apple-leaf.git
cd Apple-leaf

# 2. Setup Python backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt

# 3. Setup React frontend
cd frontend
npm install
cd ..

# 4. Download dataset (manual step required - see section below)
# Dataset must be placed in: ml-training/datasets/Apple/

# 5. Train model OR download pre-trained checkpoint
# Option A: Train (2-4 hours)
cd ml-training/classification
python train.py
cd ../..

# Option B: Download pre-trained model (recommended)
# Place densenet121_best.pth in: ml-training/checkpoints/

# 6. Start backend server (Terminal 1)
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 7. Start frontend server (Terminal 2)
cd frontend
npm run dev

# 8. Access application
# Frontend: http://localhost:5173/
# Backend: http://localhost:8000/docs
```

---

## 📁 Project Structure Analysis

```
Apple-leaf/
├── backend/                    # FastAPI backend server
│   ├── app/
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── config.py          # Configuration (MODEL_PATH, etc.)
│   │   ├── models/
│   │   │   └── disease_classifier.py  # PyTorch model wrapper
│   │   └── routes/
│   │       └── prediction.py  # API endpoints
│   ├── requirements.txt       # Python dependencies
│   └── uploads/               # Temporary image storage
│
├── frontend/                  # React + Vite frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   ├── services/api.js    # Axios API client
│   │   └── App.jsx            # Root component
│   ├── package.json           # Node.js dependencies
│   └── .env                   # Environment variables
│
├── ml-training/               # ML training pipeline
│   ├── classification/
│   │   ├── train.py          # Training script
│   │   ├── config.py         # Training config
│   │   ├── dataset.py        # Dataset loader
│   │   └── model.py          # Model architecture
│   ├── checkpoints/          # Model files (.pth) - NOT IN REPO
│   └── datasets/             # Image dataset - NOT IN REPO
│
└── docs/                     # Documentation files
```

---

## 🔑 Critical Files for AI Understanding

### 1. Backend Entry Point
**File:** `backend/app/main.py`
- FastAPI application initialization
- CORS middleware configuration
- API routes registration
- Health check endpoint

### 2. Model Configuration
**File:** `backend/app/config.py`
```python
class Settings:
    MODEL_PATH = "checkpoints/densenet121_best.pth"
    UPLOAD_DIR = "uploads"
    CLASS_NAMES = ["healthy", "rust", "scab"]
```

### 3. Disease Classifier
**File:** `backend/app/models/disease_classifier.py`
- PyTorch DenseNet121 model wrapper
- Image preprocessing pipeline
- Prediction method with confidence scores

### 4. API Routes
**File:** `backend/app/routes/prediction.py`
- POST /api/predict - Image upload and prediction
- GET /api/model/info - Model metadata
- GET /api/classes - Disease class names

### 5. Frontend API Client
**File:** `frontend/src/services/api.js`
- Axios configuration
- API endpoint wrappers
- Base URL: http://localhost:8000

### 6. Training Configuration
**File:** `ml-training/classification/config.py`
- Dataset paths
- Hyperparameters (batch_size=8, lr=0.001, epochs=50)
- Device configuration (CPU/GPU auto-detect)

---

## 📦 Dependencies Breakdown

### Python Backend Dependencies
```txt
# Core Framework
fastapi==0.100.0
uvicorn[standard]==0.23.0

# ML/AI
torch>=2.0.0
torchvision>=0.15.0
numpy>=1.24.0

# Image Processing
Pillow>=10.0.0

# API
python-multipart>=0.0.6
```

### Node.js Frontend Dependencies
```json
{
  "react": "^18.2.0",
  "vite": "^5.0.0",
  "tailwindcss": "^3.4.0",
  "axios": "^1.6.0",
  "lucide-react": "^0.294.0"
}
```

---

## 🗄️ Missing Files (Must Download Separately)

### 1. Dataset - Required for Training
**Location:** `ml-training/datasets/Apple/`  
**Source:** https://www.kaggle.com/datasets/nirmalsankalana/apple-leaf-disease-dataset  
**Size:** ~3.9 GB (4,668 images)  
**Structure:**
```
Apple/
├── train/
│   ├── healthy/ (516 images)
│   ├── rust/ (622 images)
│   └── scab/ (592 images)
├── val/ (258 images)
└── test/ (262 images)
```

**AI IDE Download Command:**
```bash
# Install Kaggle CLI
pip install kaggle

# Configure Kaggle credentials
# Create ~/.kaggle/kaggle.json with your API token

# Download dataset
kaggle datasets download -d nirmalsankalana/apple-leaf-disease-dataset -p ml-training/datasets/

# Extract
unzip ml-training/datasets/apple-leaf-disease-dataset.zip -d ml-training/datasets/Apple/
```

### 2. Pre-trained Model - Required for Running App
**Location:** `ml-training/checkpoints/densenet121_best.pth`  
**Size:** 80.5 MB  
**Alternative:** Train the model yourself (see Training section)

---

## 🚀 Detailed Setup Instructions

### Step 1: Clone and Navigate
```bash
git clone https://github.com/Gunalan183/Apple-leaf.git
cd Apple-leaf
```

### Step 2: Python Environment Setup

**Create Virtual Environment:**
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**Install Python Dependencies:**
```bash
pip install --upgrade pip
pip install -r backend/requirements.txt
```

**Expected Output:**
- Successfully installed fastapi, uvicorn, torch, torchvision, etc.
- No error messages

### Step 3: Frontend Setup

**Install Node Modules:**
```bash
cd frontend
npm install
cd ..
```

**Expected Output:**
- `node_modules/` directory created
- `package-lock.json` updated
- No vulnerability warnings (or only low-severity)

### Step 4: Dataset Preparation

**Option A: Manual Download (Recommended)**
1. Visit: https://www.kaggle.com/datasets/nirmalsankalana/apple-leaf-disease-dataset
2. Download ZIP file
3. Extract to `ml-training/datasets/Apple/`
4. Verify structure matches the tree above

**Option B: Kaggle CLI (Automated)**
```bash
pip install kaggle

# Place Kaggle API token at ~/.kaggle/kaggle.json
# Token format: {"username":"your_username","key":"your_api_key"}

kaggle datasets download -d nirmalsankalana/apple-leaf-disease-dataset
unzip apple-leaf-disease-dataset.zip -d ml-training/datasets/Apple/
```

### Step 5: Model Setup

**Option A: Train Model (2-4 hours on CPU)**
```bash
cd ml-training/classification
python train.py
```

**Training Progress Indicators:**
- Epoch 1/50 starts (~5 minutes)
- Checkpoint files appear in `ml-training/checkpoints/`
- Training loss decreases each epoch
- Validation accuracy increases to 95%+

**Option B: Use Pre-trained Model (Instant)**
- Contact repository owner for checkpoint file
- Place `densenet121_best.pth` in `ml-training/checkpoints/`

### Step 6: Verify Setup

**Check Model File Exists:**
```bash
# Windows
dir ml-training\checkpoints\densenet121_best.pth

# macOS/Linux
ls -lh ml-training/checkpoints/densenet121_best.pth
```

**Expected:** File size ~80 MB

**Check Dataset Exists:**
```bash
# Windows
dir ml-training\datasets\Apple\test\healthy\

# macOS/Linux
ls ml-training/datasets/Apple/test/healthy/
```

**Expected:** Multiple .jpg files

---

## ▶️ Running the Application

### Terminal 1: Backend Server
```bash
# Activate virtual environment
source venv/bin/activate  # Windows: .\venv\Scripts\Activate.ps1

# Navigate to backend
cd backend

# Start server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Verify Backend:**
- Open http://localhost:8000/docs
- Should see FastAPI Swagger UI
- Test /api/health endpoint

### Terminal 2: Frontend Server
```bash
# Navigate to frontend
cd frontend

# Start development server
npm run dev
```

**Expected Output:**
```
VITE v8.3.8  ready in XXX ms
➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

**Verify Frontend:**
- Open http://localhost:5173/
- Should see beautiful gradient UI
- Header shows "Apple Leaf Disease Classifier"

---

## 🧪 Testing the Application

### Test Image Upload
1. Navigate to test dataset: `ml-training/datasets/Apple/test/`
2. Choose a folder: `healthy/`, `rust/`, or `scab/`
3. Select any .jpg image
4. Drag and drop onto upload area
5. Click "Analyze Leaf"
6. Wait 2-3 seconds

### Expected Results
- **Healthy leaves**: ~95% confidence for "Healthy"
- **Rust leaves**: ~90% confidence for "Rust"
- **Scab leaves**: ~95% confidence for "Scab"

### Verification Checklist
- [ ] Image uploads successfully
- [ ] Loading indicator appears
- [ ] Results display with confidence bars
- [ ] Treatment recommendations shown
- [ ] Status badge shows disease/healthy
- [ ] Can analyze multiple images

---

## 🔧 Configuration Details

### Backend Configuration
**File:** `backend/app/config.py`

```python
import os
from pathlib import Path

class Settings:
    # Model configuration
    MODEL_PATH = os.path.join("checkpoints", "densenet121_best.pth")
    
    # Upload configuration
    UPLOAD_DIR = "uploads"
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
    
    # Model classes
    CLASS_NAMES = ["healthy", "rust", "scab"]
    
    # CORS origins (frontend URLs)
    CORS_ORIGINS = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]
```

### Frontend Configuration
**File:** `frontend/.env`

```env
VITE_API_URL=http://localhost:8000
```

**For Network Access:**
```env
VITE_API_URL=http://<YOUR_IP>:8000
```

### Training Configuration
**File:** `ml-training/classification/config.py`

```python
# Paths
DATASETS_DIR = "datasets/Apple"
CHECKPOINTS_DIR = "checkpoints"

# Hyperparameters
BATCH_SIZE = 8          # Optimized for CPU
LEARNING_RATE = 0.001
NUM_EPOCHS = 50
EARLY_STOPPING_PATIENCE = 10

# Model
MODEL_NAME = "densenet121"
PRETRAINED = True
NUM_CLASSES = 3

# Device
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
```

---

## 🐛 Common Issues and Solutions

### Issue 1: Module Not Found Error
**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # macOS/Linux

# Reinstall dependencies
pip install -r backend/requirements.txt
```

### Issue 2: Model Checkpoint Not Found
**Error:** `FileNotFoundError: Model checkpoint not found`

**Solution:**
```bash
# Option 1: Train the model
cd ml-training/classification
python train.py

# Option 2: Download pre-trained model
# Place densenet121_best.pth in ml-training/checkpoints/
```

### Issue 3: CORS Error in Browser
**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Solution:**
- Verify `frontend/.env` has correct API URL
- Restart backend server
- Check CORS_ORIGINS in `backend/app/config.py`

### Issue 4: Port Already in Use
**Error:** `Address already in use: port 8000`

**Solution:**
```bash
# Windows - Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### Issue 5: Dataset Not Found
**Error:** `FileNotFoundError: Dataset directory not found`

**Solution:**
```bash
# Verify dataset structure
ls ml-training/datasets/Apple/train/healthy/

# If empty, download dataset from Kaggle
# See Dataset Preparation section above
```

### Issue 6: Frontend Build Errors
**Error:** `Failed to resolve import`

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Issue 7: PyTorch CUDA Error
**Error:** `RuntimeError: CUDA out of memory`

**Solution:**
- Edit `ml-training/classification/config.py`
- Reduce `BATCH_SIZE` from 8 to 4 or 2
- Or use CPU mode (automatic fallback)

---

## 📊 API Endpoint Reference

### 1. Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00"
}
```

### 2. Get Model Information
```http
GET /api/model/info
```

**Response:**
```json
{
  "model": {
    "model_name": "DenseNet121",
    "num_classes": 3,
    "validation_accuracy": 0.9574,
    "device": "cpu"
  }
}
```

### 3. Get Disease Classes
```http
GET /api/classes
```

**Response:**
```json
{
  "classes": ["healthy", "rust", "scab"]
}
```

### 4. Predict Disease
```http
POST /api/predict
Content-Type: multipart/form-data
```

**Request Body:**
- `file`: Image file (JPEG/PNG, max 10MB)

**Response:**
```json
{
  "prediction": {
    "class": "scab",
    "class_display": "Scab",
    "confidence": 0.983,
    "probabilities": {
      "healthy": 0.016,
      "rust": 0.001,
      "scab": 0.983
    },
    "is_diseased": true
  }
}
```

---

## 🎓 Training Your Own Model

### Prerequisites
- Dataset downloaded and extracted
- 8GB+ RAM recommended
- 2-4 hours available (CPU training time)

### Training Command
```bash
# Activate environment
source venv/bin/activate  # Windows: .\venv\Scripts\Activate.ps1

# Navigate to classification directory
cd ml-training/classification

# Start training
python train.py
```

### Training Output
```
Epoch 1/50
Train Loss: 0.8234, Train Acc: 0.6938
Val Loss: 0.5432, Val Acc: 0.7891
Saved checkpoint: densenet121_latest.pth

Epoch 2/50
Train Loss: 0.4567, Train Acc: 0.8234
Val Loss: 0.3456, Val Acc: 0.8765
Saved checkpoint: densenet121_latest.pth

...

Epoch 6/50
Train Loss: 0.1234, Train Acc: 0.9567
Val Loss: 0.1550, Val Acc: 0.9574
New best model! Saved: densenet121_best.pth
```

### Monitor Training
```bash
# Check current epoch and accuracy
python check_checkpoint.py

# Output:
# Epoch: 6
# Validation Loss: 0.1550
# Validation Accuracy: 0.9574 (95.74%)
```

### Expected Results
- **Training Time**: 2-4 hours on CPU
- **Final Validation Accuracy**: 95%+
- **Test Accuracy**: 95%+
- **Checkpoints**: 2 files in `ml-training/checkpoints/`
  - `densenet121_best.pth` (best validation accuracy)
  - `densenet121_latest.pth` (most recent epoch)

---

## 🔍 AI IDE Integration Tips

### For Cursor/GitHub Copilot
```markdown
# Quick setup prompt for AI:
"Clone the Apple-leaf repository from GitHub, set up the Python backend with FastAPI, install the React frontend dependencies, and prepare the project for running. The dataset needs to be downloaded separately from Kaggle."
```

### For Automated Setup Scripts
```bash
#!/bin/bash
# Auto-setup script for AI IDE

echo "Setting up Apple Leaf Disease Classifier..."

# Clone repo
git clone https://github.com/Gunalan183/Apple-leaf.git
cd Apple-leaf

# Backend setup
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

# Frontend setup
cd frontend
npm install
cd ..

echo "Setup complete!"
echo "Next steps:"
echo "1. Download dataset from Kaggle"
echo "2. Place model checkpoint in ml-training/checkpoints/"
echo "3. Run 'uvicorn app.main:app' in backend/"
echo "4. Run 'npm run dev' in frontend/"
```

---

## 📚 Additional Resources

### Documentation Files
- `docs/PHASE_0_COMPLETION.md` - Project setup
- `docs/PHASE_1_COMPLETION.md` - Dataset preparation
- `docs/PHASE_2_COMPLETION.md` - Model training
- `docs/PHASE_3_COMPLETION.md` - Data augmentation

### External Links
- **Dataset**: https://www.kaggle.com/datasets/nirmalsankalana/apple-leaf-disease-dataset
- **Repository**: https://github.com/Gunalan183/Apple-leaf.git
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/
- **PyTorch Docs**: https://pytorch.org/docs/

---

## ✅ Success Checklist for AI IDE

- [ ] Repository cloned successfully
- [ ] Python virtual environment created
- [ ] Backend dependencies installed (no errors)
- [ ] Frontend dependencies installed (no errors)
- [ ] Dataset downloaded and extracted
- [ ] Model checkpoint exists (80MB file)
- [ ] Backend server starts on port 8000
- [ ] Frontend dev server starts on port 5173
- [ ] Can access http://localhost:5173/
- [ ] Can upload test image
- [ ] Prediction returns results
- [ ] Confidence scores display correctly
- [ ] Treatment recommendations appear

---

## 🎯 AI IDE Execution Summary

**Total Setup Time:** 15-20 minutes (excluding model training)  
**Active Terminals Required:** 2 (backend + frontend)  
**External Downloads Required:** 2 (dataset ~4GB, model 80MB)  
**Internet Connection:** Required for initial setup  
**Offline Capable:** Yes, after setup complete

**Automation Level:**
- ✅ Code cloning: 100% automated
- ✅ Dependency installation: 100% automated
- ⚠️ Dataset download: Manual or Kaggle CLI
- ⚠️ Model checkpoint: Manual or train
- ✅ Server startup: 100% automated

---

Made with 🤖 for AI-powered development environments

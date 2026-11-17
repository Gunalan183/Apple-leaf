# 🍎 Apple Leaf Disease Classifier

A full-stack AI-powered web application for detecting diseases in apple leaves using deep learning. Built with FastAPI, React, and PyTorch.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![React](https://img.shields.io/badge/React-18+-61DAFB.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📸 Features

- 🔬 **AI-Powered Detection**: DenseNet121 model with 95%+ accuracy
- 🎨 **Beautiful UI**: Modern gradient design with smooth animations
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile
- ⚡ **Real-time Predictions**: Get results in seconds
- 📊 **Confidence Scores**: Visual confidence meters for each prediction
- 💡 **Treatment Recommendations**: Actionable advice for each disease
- 🖼️ **Drag & Drop Upload**: Easy image upload interface

## 🦠 Detected Diseases

1. **Healthy** - No disease detected
2. **Apple Rust** - Fungal disease with orange spots
3. **Apple Scab** - Fungal disease with dark lesions

## 🏗️ Architecture

```
Apple_Leaf/
├── backend/           # FastAPI backend server
├── frontend/          # React + Vite frontend
├── ml-training/       # Model training scripts
│   ├── classification/
│   ├── checkpoints/   # Trained models (download separately)
│   └── datasets/      # Dataset (download separately)
└── docs/              # Documentation
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/downloads/)

### 1. Clone the Repository

```bash
git clone https://github.com/Gunalan183/Apple-leaf.git
cd Apple-leaf
```

### 2. Download Dataset (Required for Training)

Download the dataset from Kaggle:
👉 [Apple Leaf Disease Dataset](https://www.kaggle.com/datasets/nirmalsankalana/apple-leaf-disease-dataset)

Extract and place it in:
```
ml-training/datasets/Apple/
├── train/
│   ├── healthy/
│   ├── rust/
│   └── scab/
├── val/
│   ├── healthy/
│   ├── rust/
│   └── scab/
└── test/
    ├── healthy/
    ├── rust/
    └── scab/
```

### 3. Download Pre-trained Model (Optional - Skip Training)

If you want to skip training and use a pre-trained model:

**Option A:** Train the model yourself (see Training section below)

**Option B:** Contact the repository owner for the pre-trained checkpoint file

Place the model file:
```
ml-training/checkpoints/densenet121_best.pth
```

### 4. Set Up Backend

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
.\venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt
```

### 5. Set Up Frontend

```bash
cd frontend
npm install
cd ..
```

### 6. Start the Application

**Terminal 1 - Backend:**
```bash
# Windows
.\venv\Scripts\Activate.ps1
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# macOS/Linux
source venv/bin/activate
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 7. Access the Application

Open your browser and navigate to:
```
http://localhost:5173/
```

Backend API documentation:
```
http://localhost:8000/docs
```

## 🧪 Testing the Application

1. Navigate to the test dataset: `ml-training/datasets/Apple/test/`
2. Drag and drop an image from any disease folder
3. Click "Analyze Leaf"
4. View results with confidence scores and recommendations

## 🎓 Training Your Own Model

### Step 1: Ensure Dataset is Downloaded

Make sure you have the dataset in `ml-training/datasets/Apple/`

### Step 2: Run Training Script

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # macOS/Linux

# Navigate to classification directory
cd ml-training/classification

# Start training
python train.py
```

**Training Configuration:**
- Model: DenseNet121 (pretrained on ImageNet)
- Batch Size: 8 (optimized for CPU)
- Learning Rate: 0.001
- Max Epochs: 50
- Early Stopping: 10 epochs patience
- Expected Time: 2-4 hours on CPU

### Step 3: Monitor Training

Check saved checkpoints:
```bash
ls ml-training/checkpoints/
```

Check training progress:
```bash
python check_checkpoint.py
```

### Step 4: Evaluate Model

```bash
python evaluate.py
```

Expected results:
- **Accuracy**: 95%+
- **Precision**: 95%+
- **Recall**: 95%+
- **F1-Score**: 95%+

## 📊 Model Performance

### Baseline Model Results
- **Validation Accuracy**: 95.74%
- **Test Accuracy**: 95.04%
- **Training Dataset**: 1,210 images
- **Validation Dataset**: 258 images
- **Test Dataset**: 262 images

### Confusion Matrix
```
              Predicted
              H    R    S
Actual  H    78   0    0
        R     3   77   2
        S     1    0   101
```

## 🔧 Configuration

### Backend Configuration

Edit `backend/app/config.py`:

```python
class Settings:
    MODEL_PATH = "checkpoints/densenet121_best.pth"
    UPLOAD_DIR = "uploads"
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
```

### Frontend Configuration

Edit `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

## 🛠️ API Endpoints

### Health Check
```
GET /api/health
```

### Get Model Info
```
GET /api/model/info
```

### Get Disease Classes
```
GET /api/classes
```

### Predict Disease
```
POST /api/predict
Content-Type: multipart/form-data
Body: file (image file)
```

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

## 📁 Project Structure

```
Apple_Leaf/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration settings
│   │   ├── models/
│   │   │   └── disease_classifier.py  # ML model wrapper
│   │   ├── routes/
│   │   │   └── prediction.py    # API routes
│   │   └── schemas/
│   ├── requirements.txt         # Python dependencies
│   └── uploads/                 # Temporary upload directory
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx       # App header
│   │   │   ├── ImageUploader.jsx    # Upload component
│   │   │   └── PredictionResult.jsx # Results display
│   │   ├── pages/
│   │   │   └── Home.jsx         # Main page
│   │   ├── services/
│   │   │   └── api.js           # API client
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── .env
│
├── ml-training/
│   ├── classification/
│   │   ├── config.py            # Training configuration
│   │   ├── dataset.py           # Dataset loader
│   │   ├── model.py             # Model architecture
│   │   ├── train.py             # Training script
│   │   ├── evaluate.py          # Evaluation script
│   │   ├── transforms.py        # Data augmentation
│   │   └── visualize.py         # Visualization tools
│   ├── checkpoints/             # Model checkpoints (download)
│   └── datasets/                # Dataset (download from Kaggle)
│
├── docs/
│   ├── PHASE_0_COMPLETION.md
│   ├── PHASE_1_COMPLETION.md
│   ├── PHASE_2_COMPLETION.md
│   └── PHASE_3_COMPLETION.md
│
├── .gitignore
└── README.md
```

## 🧰 Tech Stack

### Backend
- **FastAPI** - Modern web framework for Python
- **PyTorch** - Deep learning framework
- **Torchvision** - Computer vision library
- **Pillow** - Image processing
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client
- **Lucide React** - Icon library

### Machine Learning
- **DenseNet121** - Deep convolutional neural network
- **Transfer Learning** - Pretrained on ImageNet
- **Data Augmentation** - Albumentations library

## 🐛 Troubleshooting

### Backend won't start

**Error:** "Model checkpoint not found"
```bash
# Solution: Download or train the model first
# Place it in: ml-training/checkpoints/densenet121_best.pth
```

**Error:** "ModuleNotFoundError"
```bash
# Solution: Activate venv and reinstall dependencies
.\venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
```

### Frontend won't start

**Error:** "Cannot find module"
```bash
# Solution: Reinstall node modules
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### CORS errors

**Solution:** Backend CORS is pre-configured. Verify `frontend/.env` has correct API URL.

### Port already in use

```bash
# Windows - Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

## 📚 Documentation

- [Phase 0: Project Setup](docs/PHASE_0_COMPLETION.md)
- [Phase 1: Dataset Preparation](docs/PHASE_1_COMPLETION.md)
- [Phase 2: Model Training](docs/PHASE_2_COMPLETION.md)
- [Phase 3: Data Augmentation](docs/PHASE_3_COMPLETION.md)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Dataset: [Apple Leaf Disease Dataset](https://www.kaggle.com/datasets/nirmalsankalana/apple-leaf-disease-dataset) by Nirmal Sankalana
- DenseNet Architecture: [Densely Connected Convolutional Networks](https://arxiv.org/abs/1608.06993)
- Pretrained Models: ImageNet weights from PyTorch

## 📧 Contact

- GitHub: [@Gunalan183](https://github.com/Gunalan183)
- Repository: [Apple-leaf](https://github.com/Gunalan183/Apple-leaf.git)

## 🎯 Future Enhancements

- [ ] Add more disease types
- [ ] Implement batch image processing
- [ ] Add user authentication
- [ ] Deploy to cloud platform
- [ ] Mobile application version
- [ ] REST API rate limiting
- [ ] Model performance monitoring
- [ ] A/B testing for model versions

---

Made with ❤️ and 🤖 AI

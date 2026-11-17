# 🚀 Hugging Face Spaces Deployment Guide

## 📋 Prerequisites

1. **Hugging Face Account** - [Sign up here](https://huggingface.co/join)
2. **Model Checkpoint File** - `densenet121_best.pth` (~80 MB)
3. **Git LFS Installed** - [Download here](https://git-lfs.github.com/)

---

## 🎯 Step-by-Step Deployment

### Step 1: Create a New Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Configure:
   - **Name**: `apple-leaf-classifier` (or your choice)
   - **License**: MIT
   - **SDK**: Gradio (we'll change this)
   - **Visibility**: Public (free) or Private
4. Click "Create Space"

### Step 2: Prepare Local Repository

```bash
# Navigate to your project
cd g:\Apple_Leaf

# Create .spacesconfig file (Hugging Face Spaces configuration)
# This file is already created below
```

### Step 3: Add Model Checkpoint

**IMPORTANT:** You need to add your trained model file.

```bash
# Place your model file
# Copy densenet121_best.pth to:
ml-training/checkpoints/densenet121_best.pth
```

**Note:** This file is ~80 MB and requires Git LFS (Large File Storage)

### Step 4: Initialize Git LFS

```bash
# Install Git LFS (if not already installed)
# Windows: Download from https://git-lfs.github.com/
# Mac: brew install git-lfs
# Linux: sudo apt-get install git-lfs

# Initialize Git LFS in your repo
git lfs install

# Track large files
git lfs track "*.pth"
git lfs track "ml-training/checkpoints/*.pth"

# Add .gitattributes
git add .gitattributes
git commit -m "Configure Git LFS for model files"
```

### Step 5: Build Frontend

```bash
# Navigate to frontend
cd frontend

# Install dependencies (if not already done)
npm install

# Update API URL for production
# Edit frontend/.env or frontend/.env.production:
echo "VITE_API_URL=/api" > .env.production

# Build frontend
npm run build

# Go back to root
cd ..
```

### Step 6: Add Hugging Face Remote

```bash
# Add Hugging Face Space as remote
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/apple-leaf-classifier

# Example:
# git remote add space https://huggingface.co/spaces/Gunalan183/apple-leaf-classifier
```

### Step 7: Commit All Changes

```bash
# Add all deployment files
git add app.py requirements.txt README.md .spacesconfig
git add ml-training/checkpoints/densenet121_best.pth
git add frontend/dist/
git add -A

# Commit
git commit -m "Deploy to Hugging Face Spaces"
```

### Step 8: Push to Hugging Face

```bash
# Push to Hugging Face Spaces
git push space main

# If branch name is different, use:
# git push space main:main
```

### Step 9: Wait for Build

- Go to your Space URL: `https://huggingface.co/spaces/YOUR_USERNAME/apple-leaf-classifier`
- Wait for the build to complete (~5-10 minutes)
- You'll see build logs in the Space

### Step 10: Test Your Deployment

Once deployed, your app will be available at:
```
https://YOUR_USERNAME-apple-leaf-classifier.hf.space
```

---

## 🔧 Configuration Files Explained

### 1. `.spacesconfig`
```yaml
# Hugging Face Spaces configuration
app_file: app.py
sdk: docker
sdk_version: 3.9
```

### 2. `app.py`
- Entry point for Hugging Face Spaces
- Combines FastAPI backend with React frontend
- Serves on port 7860 (Hugging Face default)

### 3. `requirements.txt`
- Python dependencies for Hugging Face runtime
- Includes FastAPI, PyTorch, and all backend needs

### 4. `.gitattributes`
```
*.pth filter=lfs diff=lfs merge=lfs -text
ml-training/checkpoints/*.pth filter=lfs diff=lfs merge=lfs -text
```

---

## 🐛 Troubleshooting

### Issue 1: Model File Too Large

**Error:** `file size exceeds GitHub's limit`

**Solution:**
```bash
# Make sure Git LFS is properly configured
git lfs install
git lfs track "*.pth"
git add .gitattributes
git commit -m "Track model with Git LFS"
```

### Issue 2: Build Fails

**Error:** `Could not find requirement.txt`

**Solution:**
- Ensure `requirements.txt` is in the root directory
- Check that all dependencies are listed

### Issue 3: Frontend Not Loading

**Error:** `404 on static files`

**Solution:**
```bash
# Rebuild frontend with correct API URL
cd frontend
echo "VITE_API_URL=/api" > .env.production
npm run build
cd ..
git add frontend/dist/
git commit -m "Update frontend build"
git push space main
```

### Issue 4: CORS Errors

**Solution:**
Update `backend/app/main.py` to allow Hugging Face domain:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://*.hf.space",  # Allow Hugging Face domains
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📦 What Gets Deployed

✅ **Backend API** (FastAPI)
✅ **Frontend UI** (React build)
✅ **Model File** (~80 MB via Git LFS)
✅ **All Python dependencies**
✅ **Static assets**

---

## 🎯 Alternative: Gradio Interface (Simpler)

If you want a simpler deployment without React frontend:

**Create `app.py` with Gradio:**
```python
import gradio as gr
from backend.app.models.disease_classifier import DiseaseClassifier

# Load model
classifier = DiseaseClassifier()

def predict(image):
    result = classifier.predict(image)
    return {
        "Class": result["class_display"],
        "Confidence": f"{result['confidence']*100:.1f}%",
        "Probabilities": result["probabilities"]
    }

# Create Gradio interface
demo = gr.Interface(
    fn=predict,
    inputs=gr.Image(type="pil"),
    outputs=[
        gr.Textbox(label="Predicted Class"),
        gr.Textbox(label="Confidence"),
        gr.JSON(label="All Probabilities")
    ],
    title="🍎 Apple Leaf Disease Classifier",
    description="Upload an apple leaf image to detect diseases"
)

demo.launch()
```

Then just:
```bash
git add app.py
git commit -m "Add Gradio interface"
git push space main
```

---

## 💡 Hugging Face Spaces Benefits

✅ **Free Forever** (for public spaces)
✅ **No Cold Starts** (always running)
✅ **Global CDN** (fast worldwide)
✅ **Automatic HTTPS**
✅ **Built-in CI/CD** (auto-deploy on push)
✅ **Community Visibility**
✅ **GPU Support Available** (paid tier)

---

## 🔗 Useful Links

- [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces)
- [Git LFS Tutorial](https://git-lfs.github.com/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

## 🎉 After Deployment

Your app will be live at:
```
https://huggingface.co/spaces/YOUR_USERNAME/apple-leaf-classifier
```

Share the link with your friends! 🚀

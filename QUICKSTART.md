# GAN-Sim-GAN - Quick Start Guide

## 🚀 Development Setup (5 Minutes)

### Prerequisites
- ✅ Python 3.14.2 installed
- ✅ Node.js v26.3.1 installed
- ✅ PowerShell (Windows)

---

## Backend Setup

### 1. Activate Python Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Start Backend Server
```powershell
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend will be available at:**
- 🏥 Health Check: http://localhost:8000/api/health
- 📚 API Docs: http://localhost:8000/docs
- 🌐 API Root: http://localhost:8000

---

## Frontend Setup

### 1. Start Frontend Server (New Terminal)
```powershell
cd frontend
npm run dev
```

**Frontend will be available at:**
- 🎨 Application: http://localhost:5173

---

## Verify Installation

### Test Backend
```powershell
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "app_name": "GAN-Sim-GAN",
  "version": "1.0.0",
  "model_available": false
}
```

**Note:** `model_available: false` is expected until model training is completed in PHASE 2.

---

## Project Status

**Current Phase:** PHASE 0 ✅ COMPLETED

### Completed:
- ✅ Project structure created
- ✅ Python dependencies installed
- ✅ Node.js dependencies installed
- ✅ Backend server tested and working
- ✅ Frontend server tested and working
- ✅ Configuration files ready

### Next Phase: PHASE 1 - Dataset Download and Preparation

---

## File Structure

```
GAN-Sim-GAN/
├── backend/          # FastAPI Python backend
├── frontend/         # React + Vite frontend
├── ml-training/      # ML model training scripts
├── docs/             # Documentation
├── venv/             # Python virtual environment
└── README.md         # Full documentation
```

---

## Common Commands

### Backend
```powershell
# Activate environment
.\venv\Scripts\Activate.ps1

# Run server
cd backend
python -m uvicorn app.main:app --reload

# Install new package
pip install package-name
pip freeze > requirements.txt
```

### Frontend
```powershell
# Run dev server
cd frontend
npm run dev

# Build for production
npm run build

# Install new package
npm install package-name
```

---

## Troubleshooting

### Backend won't start
1. Make sure virtual environment is activated
2. Check if port 8000 is available
3. Run from `backend/` directory, not root

### Frontend won't start
1. Make sure you're in `frontend/` directory
2. Check if port 5173 is available
3. Try `npm install` if dependencies are missing

---

## Documentation

- **Full README**: `README.md`
- **PHASE 0 Report**: `docs/PHASE_0_COMPLETION.md`
- **API Documentation**: http://localhost:8000/docs (when server running)

---

**Ready to build amazing AI-powered agriculture technology! 🌿🤖**

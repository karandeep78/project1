# Phishing Detector - Setup Guide

This guide will help you set up the Phishing Detector application with all dependencies and compatibility fixes.

## Quick Setup

### For macOS/Linux:
```bash
chmod +x setup.sh
./setup.sh
```

### For Windows:
```cmd
setup.bat
```

## Manual Setup

### 1. Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python app.py
```

The application will be available at: **http://localhost:5001**

## Important Notes

### Compatibility Fixes

This project includes compatibility fixes for scikit-learn version mismatches:

1. **sklearn_compat.py**: Handles compatibility between older model files (trained with sklearn 1.3.1) and newer sklearn versions (1.5.2)
   - Fixes missing `_gb_losses` module
   - Adds `monotonic_cst` attribute to DecisionTreeRegressor
   - Reconstructs loss objects for GradientBoosting models

2. **app.py**: Automatically applies compatibility patches when loading the model

3. **feature.py**: Includes performance optimizations:
   - Timeouts for external API calls
   - Fixed bugs in feature extraction
   - Optimized slow operations

4. **convert.py**: Includes phishing pattern detection:
   - Detects IP-like domains
   - Detects domain names in URL paths
   - Overrides model predictions for obvious phishing patterns

### Dependencies

All dependencies are pinned to specific versions in `requirements.txt`:
- Flask==3.0.3
- scikit-learn==1.5.2
- numpy==1.26.4
- pandas==2.2.2
- And others...

### Troubleshooting

**Port 5000 already in use (macOS):**
- The app automatically uses port 5001 to avoid conflicts with AirPlay

**Model loading errors:**
- The compatibility shim (`sklearn_compat.py`) should handle most issues automatically
- If you see errors, make sure all dependencies are installed correctly

**Slow feature extraction:**
- The code has been optimized to reduce extraction time from 78s to ~5s
- Some external API calls (Google Index, Alexa, PageRank) have been disabled for speed

## Project Information

- **College**: CGC Landran College
- **Students**: Karan, Janakpreet, Jaskaran
- **Guide**: Ms. Anjali Thakur

## Support

If you encounter any issues, check:
1. Python version (3.8+ recommended)
2. All dependencies are installed
3. Virtual environment is activated
4. Model file (`newmodel.pkl`) exists in the project directory

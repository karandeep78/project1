# Phishing Detector

A machine learning-based web application to detect phishing URLs and protect users from malicious websites.

## Features

- **Real-time URL Analysis**: Analyze any URL to determine if it's safe or potentially phishing
- **Machine Learning Model**: Uses Gradient Boosting Classifier trained on 30 features
- **Fast Processing**: Optimized feature extraction (5-10 seconds per URL)
- **Pattern Detection**: Advanced heuristics to catch obvious phishing patterns
- **User-Friendly Interface**: Clean, modern web interface

## Quick Start

### Automatic Setup (Recommended)

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

### Manual Setup

1. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the application:**
   Open your browser and go to: http://localhost:5001

## Project Structure

```
Phishing-detector/
├── app.py                 # Main Flask application
├── feature.py             # Feature extraction module
├── convert.py             # URL conversion and pattern detection
├── sklearn_compat.py      # Compatibility fixes for sklearn
├── newmodel.pkl           # Trained ML model
├── requirements.txt       # Python dependencies
├── setup.sh              # Setup script (macOS/Linux)
├── setup.bat             # Setup script (Windows)
├── templates/            # HTML templates
│   ├── index.html
│   └── usecases.html
└── static/              # Static assets (CSS, JS, images)
```

## Compatibility Notes

This project includes automatic compatibility fixes for:
- **scikit-learn version mismatch**: Model was trained with sklearn 1.3.1, but works with 1.5.2
- **Port conflicts**: Automatically uses port 5001 on macOS (to avoid AirPlay conflict)
- **Performance**: Optimized slow feature extraction operations

All fixes are handled automatically by `sklearn_compat.py` and `app.py`.

## Dependencies

- Flask 3.0.3
- scikit-learn 1.5.2
- numpy 1.26.4
- pandas 2.2.2
- beautifulsoup4 4.12.3
- Requests 2.31.0
- And others (see requirements.txt)

## Project Information

- **Institution**: CGC Landran College
- **Students**: Karan, Janakpreet, Jaskaran
- **Guide**: Ms. Anjali Thakur
- **Year**: 2024

## Troubleshooting

### Port Already in Use
The app automatically uses port 5001. If you need a different port, edit `app.py`:
```python
app.run(debug=True, port=5001)  # Change port number here
```

### Model Loading Errors
Make sure `sklearn_compat.py` is in the same directory as `app.py`. The compatibility shim handles version mismatches automatically.

### Slow Performance
Feature extraction has been optimized. If still slow, check your internet connection as some features require external API calls.

## License

Final Year Project © 2024. All Rights Reserved.

## Support

For issues or questions, refer to the SETUP_GUIDE.md file.

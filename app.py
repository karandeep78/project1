#importing required libraries

import os
from flask import Flask, request, render_template, jsonify
import numpy as np
import pandas as pd
from sklearn import metrics
import warnings
import pickle
import joblib
# Import compatibility shim before loading model
try:
    import sklearn_compat
except:
    pass
from convert import convertion
warnings.filterwarnings('ignore')
from feature import FeatureExtraction

# Try loading with joblib first (better compatibility), fallback to pickle
try:
    gbc = joblib.load("newmodel.pkl")
except:
    file = open("newmodel.pkl","rb")
    gbc = pickle.load(file)
    file.close()

# Patch the model to fix compatibility issues with newer sklearn versions
try:
    from sklearn_compat import patch_tree_estimators
    from sklearn._loss.loss import HalfBinomialLoss
    from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
    
    # Fix loss object if it's a MockLoss
    if hasattr(gbc, '_loss') and type(gbc._loss).__name__ == 'MockLoss':
        loss_name = getattr(gbc, 'loss', 'deviance')
        n_classes = getattr(gbc, 'n_classes_', None)
        if loss_name == 'deviance' or loss_name == 'log_loss':
            if n_classes == 2:
                gbc._loss = HalfBinomialLoss()
            else:
                from sklearn._loss.loss import HalfMultinomialLoss
                gbc._loss = HalfMultinomialLoss(n_classes)
    
    # Fix monotonic_cst attribute for all tree estimators
    gbc = patch_tree_estimators(gbc)
except Exception as e:
    import warnings
    warnings.warn(f"Could not patch model: {e}")
    pass


app = Flask(__name__)


def _scan_url(url):
    obj = FeatureExtraction(url)
    x = np.array(obj.getFeaturesList()).reshape(1, 30)
    y_pred = gbc.predict(x)[0]
    return convertion(url, int(y_pred))


def _cors_headers(response):
    origin = os.environ.get("CORS_ORIGIN", "*")
    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@app.after_request
def add_cors(response):
    if request.path.startswith("/api/"):
        return _cors_headers(response)
    return response


@app.route("/api/scan", methods=["POST", "OPTIONS"])
def api_scan():
    if request.method == "OPTIONS":
        return "", 204
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or request.form.get("name") or "").strip()
    if not url:
        return jsonify({"error": "url is required"}), 400
    try:
        name = _scan_url(url)
        return jsonify(
            {
                "url": name[0],
                "verdict": name[1],
                "buttonText": name[2],
                "isSafe": len(name) > 3,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#from flask import Flask, render_template, request
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/result", methods=["POST", "GET"])
def predict():
    if request.method == "POST":
        url = request.form["name"]
        name = _scan_url(url)
        return render_template("index.html", name=name)
@app.route('/usecases', methods=['GET', 'POST'])
def usecases():
    return render_template('usecases.html')
if __name__ == "__main__":
    app.run(debug=True, port=5001)

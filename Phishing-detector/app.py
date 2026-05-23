#importing required libraries

from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn import metrics
import warnings
import pickle
import joblib
from pathlib import Path
# Import compatibility shim before loading model
try:
    import sklearn_compat
except:
    pass
from convert import convertion
warnings.filterwarnings('ignore')
from feature import FeatureExtraction

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "newmodel.pkl"

# Try loading with joblib first (better compatibility), fallback to pickle
try:
    gbc = joblib.load(MODEL_PATH)
except:
    file = open(MODEL_PATH,"rb")
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
#from flask import Flask, render_template, request
@app.route("/")
def home():
    return render_template("index.html")
@app.route('/result',methods=['POST','GET'])
def predict():
    if request.method == "POST":
        url = request.form["name"]
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1,30)
    
        y_pred =gbc.predict(x)[0]
            #1 is safe
            #-1 is unsafe
        #y_pro_phishing = gbc.predict_proba(x)[0,0]
        #y_pro_non_phishing = gbc.predict_proba(x)[0,1]
            # if(y_pred ==1 ):
        #3pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
        #xx =y_pred
        name=convertion(url,int(y_pred))
        return render_template("index.html", name=name)
@app.route('/usecases', methods=['GET', 'POST'])
def usecases():
    return render_template('usecases.html')
if __name__ == "__main__":
    app.run(debug=True, port=5001)

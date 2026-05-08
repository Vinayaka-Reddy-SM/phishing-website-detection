from flask import Flask, render_template, request
import pickle
import numpy as np
import os

app = Flask(__name__)

# Ensure we are in the right directory to find the model
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load model
model = pickle.load(open("model.pkl", "rb"))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Expected inputs: URL Length, HTTPS (1 or 0)
        # request.form.values() returns the values in order of the HTML form
        features = [float(x) for x in request.form.values()]
        final_features = [np.array(features)]

        prediction = model.predict(final_features)

        if prediction[0] == 1:
            result = "Safe Website"
            status = "safe"
        else:
            result = "Phishing Website"
            status = "phishing"

        return render_template("index.html", prediction_text=result, status=status)

    except Exception as e:
        print(f"Error: {e}")
        return render_template("index.html", prediction_text="Invalid Input", status="error")

if __name__ == "__main__":
    app.run(debug=True)

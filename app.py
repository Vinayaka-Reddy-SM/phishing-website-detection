from flask import Flask, render_template, request
import pickle
import numpy as np
import os
import re
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Ensure we are in the right directory to find the model
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Database initialization
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scans
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  url TEXT, 
                  result TEXT, 
                  status TEXT,
                  timestamp DATETIME)''')
    conn.commit()
    conn.close()

init_db()

# Load model
model = pickle.load(open("model.pkl", "rb"))

def extract_features(url):
    """
    Extracts features from a URL to match the training data:
    URL_Length, HTTPS, Has_At, Dot_Count, Is_Shortened, Digit_Count
    """
    url_length = len(url)
    has_https = 1 if url.startswith("https") else 0
    has_at = 1 if "@" in url else 0
    dot_count = url.count(".")
    shortening_services = r"bit\.ly|goo\.gl|tinyurl\.com|t\.co|rebrand\.ly|is\.gd|buff\.ly"
    is_shortened = 1 if re.search(shortening_services, url) else 0
    digit_count = sum(c.isdigit() for c in url)
    return [url_length, has_https, has_at, dot_count, is_shortened, digit_count]

@app.route('/')
def home():
    # Fetch recent scans from database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT url, result, status, timestamp FROM scans ORDER BY timestamp DESC LIMIT 5")
    history = c.fetchall()
    conn.close()
    return render_template("index.html", history=history)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        url = request.form.get("url", "").strip()
        if not url:
            return render_template("index.html", prediction_text="Please enter a URL", status="error")

        if not url.startswith("http"):
            url = "http://" + url

        features = extract_features(url)
        final_features = [np.array(features)]
        prediction = model.predict(final_features)
        
        reasons = []
        if features[1] == 0: reasons.append("Missing HTTPS encryption.")
        if features[2] == 1: reasons.append("Contains suspicious '@' symbol.")
        if features[4] == 1: reasons.append("Uses a URL shortening service.")
        if features[5] > 10: reasons.append("Contains an unusual number of digits.")
        if features[3] > 3: reasons.append("Too many dots in the URL structure.")

        if prediction[0] == 1:
            result = "Safe Website"
            status = "safe"
            description = "Our AI analysis indicates this website follows standard security patterns."
        else:
            result = "Phishing Website"
            status = "phishing"
            description = f"Potential threats detected: {', '.join(reasons) if reasons else 'Suspicious patterns found.'}"

        # Save to database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO scans (url, result, status, timestamp) VALUES (?, ?, ?, ?)",
                  (url, result, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        
        # Fetch updated history
        c.execute("SELECT url, result, status, timestamp FROM scans ORDER BY timestamp DESC LIMIT 5")
        history = c.fetchall()
        conn.close()

        return render_template("index.html", 
                               prediction_text=result, 
                               status=status, 
                               url=url, 
                               description=description,
                               features=features,
                               history=history)

    except Exception as e:
        print(f"Error: {e}")
        return render_template("index.html", prediction_text="Invalid Input", status="error")

if __name__ == "__main__":
    app.run(debug=True)

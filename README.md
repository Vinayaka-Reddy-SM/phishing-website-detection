# Phishing Website Detection Using Machine Learning

A modern web application that detects phishing URLs using a Random Forest machine learning model.

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have **Python 3.11+** installed on your system.

### 2. Installation
Navigate to the project directory and install the required libraries:
```bash
cd Phishing-Website-Detection
pip install -r requirements.txt
```

### 3. Training the Model
If the `model.pkl` file is missing or you want to retrain the model with the latest data:
```bash
python train_model.py
```

### 4. Running the Web Application
Start the Flask server:
```bash
python app.py
```

### 5. Access the App
Open your web browser and go to:
**[http://127.0.0.1:5000](http://127.0.0.1:5000)**

## 🛠️ Project Features
- **Machine Learning**: Uses Scikit-learn's Random Forest Classifier.
- **Frontend**: Premium UI built with HTML5/CSS3 using Glassmorphism.
- **Backend**: Flask web framework.
- **Deployment Ready**: Configured for Render/Railway with `Procfile`.

## 📂 Folder Structure
- `app.py`: Main Flask application.
- `train_model.py`: Model training script.
- `phishing.csv`: Training dataset.
- `model.pkl`: Serialized ML model.
- `static/style.css`: Modern styling.
- `templates/index.html`: Web interface.

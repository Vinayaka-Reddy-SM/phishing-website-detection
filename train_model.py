import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os

# Ensure we are in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load dataset
data = pd.read_csv("phishing.csv")

# Features and labels
X = data.drop("Label", axis=1)
y = data["Label"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Check accuracy
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Model trained successfully. Accuracy: {accuracy * 100:.2f}%")

# Save model
pickle.dump(model, open("model.pkl", "wb"))
print("Model saved as model.pkl")

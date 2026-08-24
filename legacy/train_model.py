import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load Dataset
data = pd.read_csv("dataset/placement_data.csv")

# Input Features
X = data[["CGPA", "DSA", "Projects", "Internship", "Communication"]]

# Target
y = data["Placed"]

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train Model
model = RandomForestClassifier()

model.fit(X_train, y_train)

# Save Model
joblib.dump(model, "model.pkl")

print("Model trained successfully!")
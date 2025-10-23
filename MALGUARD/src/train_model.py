# src/train_model.py
import os
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from model_utils import URLModelHelper
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# Locate dataset
base_dir = os.path.dirname(__file__)
data_path = os.path.join(base_dir, '..', 'data', 'real_urls.csv')

if not os.path.exists(data_path):
    raise FileNotFoundError(f"❌ Dataset not found at {data_path}. Run fetch_real_data.py first!")

print(f"✅ Using dataset from: {data_path}")

# Load dataset
df = pd.read_csv(data_path)

if 'url' not in df.columns or 'label' not in df.columns:
    raise ValueError("CSV must contain 'url' and 'label' columns.")

urls = df['url'].astype(str).tolist()
y = df['label'].values

# Initialize helper and extract features
helper = URLModelHelper()
X = helper.fit_transform_urls(urls)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)

# Evaluate
preds = clf.predict(X_test)
print("\n=== Classification Report ===")
print(classification_report(y_test, preds))

# Save model
models_dir = os.path.join(base_dir, '..', 'models')
os.makedirs(models_dir, exist_ok=True)
model_path = os.path.join(models_dir, 'url_model.joblib')
joblib.dump({'helper': helper, 'clf': clf}, model_path)

print(f"\n✅ Saved model to {model_path}")

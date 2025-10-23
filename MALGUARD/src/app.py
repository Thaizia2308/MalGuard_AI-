from flask import Flask, request, render_template, jsonify
import joblib
import os
import requests
from dotenv import load_dotenv
# ------------------------------------------------------------
# 🔹 Load environment variables (BOM-safe)
# ------------------------------------------------------------
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(env_path):
    with open(env_path, encoding='utf-8-sig') as f:  # utf-8-sig ignores BOM
        for line in f:
            line = line.strip()
            if line and '=' in line and not line.startswith('#'):
                key, val = line.split('=', 1)
                os.environ['FLASK_SKIP_DOTENV'] = '1'

# ------------------------------------------------------------
# 🔹 Flask app
# ------------------------------------------------------------
app = Flask(__name__)

# ------------------------------------------------------------
# 🔹 Load your trained ML model
# ------------------------------------------------------------
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'url_model.joblib')

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

model_bundle = joblib.load(MODEL_PATH)
helper = model_bundle['helper']
clf = model_bundle['clf']

# ------------------------------------------------------------
# 🔹 Google Safe Browsing (Real-time check)
# ------------------------------------------------------------
def check_google_safe_browsing(url: str):
    api_key = os.getenv("GOOGLE_SAFE_BROWSING_KEY")
    if not api_key:
        return None  # Skip if key not provided

    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"

    body = {
        "client": {"clientId": "malguard-ai", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE",
                "POTENTIALLY_HARMFUL_APPLICATION"
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        },
    }

    try:
        response = requests.post(endpoint, json=body, timeout=10)
        result = response.json()
        return "matches" in result
    except Exception as e:
        print(f"⚠️ Google Safe Browsing error: {e}")
        return None

# ------------------------------------------------------------
# 🔹 Home page
# ------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

# ------------------------------------------------------------
# 🔹 API endpoint
# ------------------------------------------------------------
@app.route('/api/check', methods=['POST'])
def check():
    data = request.get_json(force=True)
    url = data.get('url', '').strip()

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        # Step 1: Google Safe Browsing check
        live_check = check_google_safe_browsing(url)
        if live_check is True:
            return jsonify({
                'url': url,
                'label': 1,
                'source': 'Google Safe Browsing',
                'message': '❌ Malicious (Verified by Google Safe Browsing)'
            })

        # Step 2: Local AI model prediction
        X = helper.transform_urls([url])
        prob = clf.predict_proba(X)[0][1]
        label = int(prob > 0.5)

        return jsonify({
            'url': url,
            'malicious_probability': round(float(prob), 3),
            'label': label,
            'source': 'AI Model',
            'message': '✅ Safe' if label == 0 else '❌ Malicious (Predicted by AI)'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ------------------------------------------------------------
# 🔹 Run Flask app
# ------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)

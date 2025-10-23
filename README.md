MalGuard AI

MalGuard AI is an AI-powered URL safety checker that helps detect whether a given website link (URL) is safe or malicious. It uses machine learning and external APIs to classify URLs and provide security insights.

🚀 Features

Detects malicious and phishing URLs.

Provides detailed analysis of website safety.

Uses AI/ML models for intelligent detection.

Easy to use via a simple interface.

Logs analysis results for future reference.

🛠️ Tech Stack

Python 3.10+

Flask – for building the web application.

Pandas & NumPy – for data handling.

Scikit-learn – for ML model training.

Requests / HTTPX – for making API calls.

Google Safe Browsing API – for URL threat intelligence.

VS Code – recommended IDE for running and editing the project.

📁 Project Structure
MalGuard/
│
├─ src/
│   ├─ app.py           # Main Flask app
│   ├─ train_model.py   # Script to train ML model
│   ├─ utils.py         # Helper functions
│   └─ ...
│
├─ data/                # Dataset folder
├─ models/              # Trained ML models
├─ requirements.txt     # Python dependencies
└─ .env                 # Environment variables (API keys, etc.)

⚡ Prerequisites

Make sure you have:

Python 3.10+ installed

Git installed

VS Code installed

A Google Safe Browsing API key (store it in .env file)

💻 How to Run on VS Code

Clone the Repository

git clone https://github.com/Thaizia2308/MalGuard_AI-.git
cd MalGuard_AI-


Create a Virtual Environment

python -m venv .venv


Activate the Virtual Environment

Windows:

.venv\Scripts\activate


Linux / MacOS:

source .venv/bin/activate


Install Dependencies

pip install -r requirements.txt


Set Environment Variables

Create a .env file in the project root:

GOOGLE_SAFE_BROWSING_KEY=YOUR_API_KEY_HERE


Run the Flask App

python src/app.py


Open your browser and go to: http://127.0.0.1:5000

🧠 Training the Model (Optional)

If you want to train/update the AI model:

python src/train_model.py


Make sure your dataset is in the data/ folder.

📌 Notes

Always use a virtual environment to avoid package conflicts.

Keep your API keys secure in the .env file.

The app can be extended to include real-time URL scanning.

👨‍💻 Author

Thaizia – GitHub

📄 License

MIT License

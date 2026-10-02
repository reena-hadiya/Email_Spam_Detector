import os
import joblib
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')
MODEL_DIR = os.path.join(BASE_DIR, '..', 'models')

# Initialize Flask with static folder pointing to frontend
app = Flask(__name__, static_folder=FRONTEND_DIR)
CORS(app)

MODEL_PATH = os.path.join(MODEL_DIR, 'spam_model.pkl')
VECTORIZER_PATH = os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl')

# Load model and vectorizer
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

@app.route('/', methods=['GET'])
def home():
    return send_from_directory(FRONTEND_DIR, 'index.html')

# 2. Serve static files (style.css, script.js)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(FRONTEND_DIR, filename)

# 3. Handle prediction requests from frontend
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(silent=True) or {}
    email_text = data.get('email_text', '').strip()
    
    if not email_text:
        return jsonify({'error': 'Email text cannot be empty'}), 400

    # Vectorize input and predict
    text_vec = vectorizer.transform([email_text])
    prediction = int(model.predict(text_vec)[0])
    probabilities = model.predict_proba(text_vec)[0]
    
    spam_prob = round(float(probabilities[1]) * 100, 2)
    ham_prob = round(float(probabilities[0]) * 100, 2)
    
    return jsonify({
        'result': 'Spam' if prediction == 1 else 'Not Spam',
        'is_spam': prediction == 1,
        'spam_probability': spam_prob,
        'not_spam_probability': ham_prob
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)
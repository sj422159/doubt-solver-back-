<<<<<<< HEAD
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure CORS (restrict to specific origins in production)
CORS(app, resources={r"/chat": {"origins": "https://your-frontend-domain.com"}})

# Load API key from environment variable
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    raise RuntimeError("MISTRAL_API_KEY environment variable is not set")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        payload = {
            "model": "mistral-large-latest",
            "messages": [
                {"role": "system", "content": "You are an AI teacher."},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {MISTRAL_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload
        )
        
        logger.info(f"Status Code: {response.status_code}")
        logger.debug(f"Response Body: {response.text}")
        
        if response.status_code != 200:
            logger.error(f"API Error: {response.status_code} - {response.text}")
            return jsonify({"error": f"API Error: {response.status_code}"}), 500
        
        result = response.json()
        reply = result.get("choices", [{}])[0].get("message", {}).get("content", "No response")
        return jsonify({"reply": reply})

    except requests.exceptions.RequestException as e:
        logger.error(f"Request Exception: {str(e)}")
        return jsonify({"error": "API Request Error"}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "Unexpected error"}), 500

if __name__ == '__main__':
    # Use a production WSGI server like gunicorn to run the app
    app.run(debug=False, host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
=======
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

MISTRAL_API_KEY = "0ezXEjX0u9zxCMPamqQyBBI9yxqwpzoQ"  # Replace with your actual API key

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Updated request format according to Mistral API documentation
        payload = {
            "model": "mistral-large-latest",  # Updated model name
            "messages": [
                {"role": "system", "content": "You are an AI teacher."},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {MISTRAL_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload
        )
        
        # Print response for debugging
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code != 200:
            return jsonify({"error": f"API Error: {response.status_code} - {response.text}"}), 500
        
        result = response.json()
        reply = result.get("choices", [{}])[0].get("message", {}).get("content", "No response")
        return jsonify({"reply": reply})

    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {str(e)}")
        return jsonify({"error": f"API Request Error: {str(e)}"}), 500
    except Exception as e:
        print(f"General Exception: {str(e)}")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
>>>>>>> f88e84de4d88bc3982162655c9307dc0494c87b3

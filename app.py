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
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai, os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)  # Cho phép tất cả domain truy cập để test

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "✅ Backend is alive"})

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "")
        if not message:
            return jsonify({"error": "No message provided"}), 400

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Bạn là ThamAI"},
                {"role": "user", "content": message}
            ]
        )
        return jsonify({"reply": response.choices[0].message["content"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

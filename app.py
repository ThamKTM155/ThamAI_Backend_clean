from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import openai
import os

# Nạp biến môi trường từ file .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Khởi tạo Flask app
app = Flask(__name__)

# Cho phép CORS từ các domain frontend của Vercel
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://thach-ai-frontend-fresh.vercel.app",
            "https://thach-ai-frontend-fresh-ub7q-7gxu3puj2-thamktm155s-projects.vercel.app"
        ]
    }
})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"response": "⚠️ Bạn chưa nhập tin nhắn nào cả."}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là trợ lý ảo ThamAI"},
                {"role": "user", "content": message}
            ]
        )
        reply = response.choices[0].message["content"].strip()
        return jsonify({"response": reply})
    
    except Exception as e:
        print("❌ Lỗi khi gọi OpenAI:", e)
        return jsonify({"response": "⚠️ Đã xảy ra lỗi khi gọi OpenAI."}), 500

# Chạy app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# Nạp biến môi trường từ file .env
load_dotenv()

# Khởi tạo Flask app
app = Flask(__name__)

# Chỉ cho phép frontend chính thức gọi backend
CORS(app, origins=["https://thach-ai-frontend-fresh.vercel.app"])

# Thiết lập API Key OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ Route kiểm tra kết nối backend
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "✅ ThamAI backend is running."})

# ✅ Route chính xử lý chat
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "⚠️ Bạn chưa nhập tin nhắn nào cả."})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"response": reply})
    except Exception as e:
        print("❌ Lỗi gọi OpenAI:", e)
        return jsonify({"response": "⚠️ Đã xảy ra lỗi khi gọi OpenAI."})
        
# Khởi chạy ứng dụng Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

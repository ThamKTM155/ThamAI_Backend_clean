from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import openai
import os
import traceback

# Nạp biến môi trường từ file .env (chỉ dùng khi chạy local)
load_dotenv()

# Lấy API key từ biến môi trường
openai.api_key = os.getenv("OPENAI_API_KEY")

# Khởi tạo Flask app
app = Flask(__name__)

# Cho phép frontend gọi API (có thể thêm nhiều origin nếu cần)
CORS(app, origins=[
    "https://thach-ai-frontend-fresh.vercel.app",
    "https://thach-ai-frontend-fresh-2gh5quauy-thamktm155s-projects.vercel.app"
])

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Lấy dữ liệu JSON từ request
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"response": "⚠️ Không nhận được tin nhắn."}), 400

        message = data["message"]

        # Kiểm tra API key trước khi gọi OpenAI
        if not openai.api_key:
            return jsonify({"response": "⚠️ Thiếu API key của OpenAI trên server."}), 500

        # Gọi API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là trợ lý ảo ThamAI"},
                {"role": "user", "content": message}
            ]
        )

        # Lấy câu trả lời
        reply = response.choices[0].message.content.strip()
        return jsonify({"response": reply})

    except Exception as e:
        # In lỗi ra log Render để dễ debug
        print("❌ Lỗi khi xử lý yêu cầu:", e)
        print(traceback.format_exc())
        return jsonify({"response": f"⚠️ Lỗi server: {str(e)}"}), 500


if __name__ == "__main__":
    # Chạy local
    app.run(host="0.0.0.0", port=5000)


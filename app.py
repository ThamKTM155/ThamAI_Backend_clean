from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# 1. Nạp biến môi trường từ file .env
load_dotenv()

# 2. Lấy API key từ biến môi trường
openai.api_key = os.getenv("OPENAI_API_KEY")

# 3. Khởi tạo Flask app + bật CORS cho tất cả domain
app = Flask(__name__)
CORS(app)  # Cho phép mọi domain gọi backend

# 4. Route kiểm tra server
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "✅ ThamAI backend is running."})

# 5. Route chat
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "⚠️ Bạn chưa nhập tin nhắn."}), 400

        # Gọi API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Bạn là ThamAI, trợ lý ảo hỗ trợ người dùng."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=200,
            temperature=0.7
        )

        ai_reply = response.choices[0].message["content"].strip()
        return jsonify({"reply": ai_reply})

    except Exception as e:
        # Log lỗi chi tiết vào console
        print("❌ Lỗi khi gọi OpenAI API:", str(e))
        return jsonify({"error": "⚠️ Đã xảy ra lỗi khi xử lý yêu cầu."}), 500

# 6. Chạy ứng dụng khi local
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from openai import OpenAI

# 1. Nạp biến môi trường từ file .env (khi chạy local)
load_dotenv()

# 2. Khởi tạo Flask app
app = Flask(__name__)

# 3. Lấy URL frontend từ biến môi trường (mặc định cho phép tất cả để test)
frontend_url = os.getenv("FRONTEND_URL", "*")
CORS(app, resources={r"/*": {"origins": frontend_url}})

# 4. Lấy khóa API từ biến môi trường
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY chưa được thiết lập trong biến môi trường.")

# 5. Khởi tạo OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# 6. Route kiểm tra server hoạt động
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "success",
        "message": "✅ ThamAI backend is running.",
        "frontend_allowed": frontend_url
    })

# 7. Route xử lý chat
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)  # force=True để tự parse JSON
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # Gọi API OpenAI (model mới)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Bạn là ThamAI, trợ lý ảo hỗ trợ người dùng."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )

        ai_reply = response.choices[0].message.content.strip()

        return jsonify({
            "status": "success",
            "reply": ai_reply
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# 8. Chạy local
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)

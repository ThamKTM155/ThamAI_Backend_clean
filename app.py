from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

# 1. Nạp biến môi trường
load_dotenv()

# 2. Khởi tạo Flask app
app = Flask(__name__)
CORS(app, origins="*")  # Cho phép tất cả domain

# ⚠️ Nếu muốn chặt chẽ thì thay "*" bằng domain frontend của anh:
#    "https://thach-ai-frontend-fresh.vercel.app"
CORS(app, resources={r"/*": {"origins": "*"}})

# 3. Khởi tạo OpenAI client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ Thiếu OPENAI_API_KEY trong file .env")

client = OpenAI(api_key=OPENAI_API_KEY)

# 4. Route kiểm tra server
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "✅ Phần phụ trợ ThamAI đang chạy."})

# 5. Route test
@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "⚡ Test OK"})

# 6. Route chat
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"error": "⚠️ Bạn chưa nhập tin nhắn."}), 400

    try:
       resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Bạn là ThamAI, trợ lý ảo thân thiện, nói tiếng Việt."},
                {"role": "user", "content": user_message},
            ],
            temperature=0.7,
            max_tokens=500,
        )

        reply = resp.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        print("❌ OpenAI error:", str(e))
        return jsonify({"error": str(e)}), 500


# 7. Khi chạy local thì bật app.run(), còn khi deploy Render thì KHÔNG bật
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

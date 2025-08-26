from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

# =========================
# 1. Load biến môi trường từ file .env
# =========================
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ Thiếu OPENAI_API_KEY trong file .env")

# =========================
# 2. Khởi tạo Flask app
# =========================
app = Flask(__name__)

# Cho phép gọi API từ bất kỳ domain nào (local test & Vercel)
CORS(app, resources={r"/*": {"origins": "*"}})

# =========================
# 3. Khởi tạo OpenAI client
# =========================
client = OpenAI(api_key=OPENAI_API_KEY)

# =========================
# 4. Route kiểm tra server
# =========================
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "✅ ThamAI backend is running."})

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "⚡ Test OK"})

# =========================
# 5. Route chính xử lý chat
# =========================
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}
        user_message = (data.get("message") or "").strip()

        if not user_message:
            return jsonify({"error": "⚠️ Bạn chưa nhập tin nhắn."}), 400

        # Gọi API OpenAI
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Bạn là ThamAI, trợ lý ảo thân thiện, hữu ích, nói tiếng Việt."},
                {"role": "user", "content": user_message},
            ],
            temperature=0.7,
            max_tokens=500,
        )

        reply = resp.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        print("❌ OpenAI error:", str(e))
        return jsonify({"error": f"Lỗi OpenAI: {str(e)}"}), 500

# =========================
# 6. Chạy server local (debug)
# =========================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

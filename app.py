from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import openai
import os

# Nạp biến môi trường từ file .env
load_dotenv()

# Lấy API key từ biến môi trường
openai.api_key = os.getenv("OPENAI_API_KEY")

# Khởi tạo Flask app
app = Flask(__name__)

# Chỉ cho phép gọi từ frontend của anh (Vercel)
CORS(app, origins=["https://thach-ai-frontend-fresh-ub7q-kix23g715-thamktm155s-projects.vercel.app"])

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"response": "⚠️ Bạn chưa nhập tin nhắn nào cả."})

    try:
        # Gọi API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là trợ lý ảo ThamAI, luôn trả lời lịch sự và dễ hiểu."},
                {"role": "user", "content": message}
            ]
        )

        reply = response['choices'][0]['message']['content'].strip()
        return jsonify({"response": reply})

    except Exception as e:
        print("❌ Lỗi khi gọi OpenAI:", e)
        return jsonify({"response": "⚠️ Đã xảy ra lỗi khi gọi OpenAI."})

# Chạy ứng dụng Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

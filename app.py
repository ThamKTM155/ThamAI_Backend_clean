import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import openai

# Nạp biến môi trường từ file .env
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Khởi tạo Flask app
app = Flask(__name__)

# Chỉ cho phép frontend chính thức gọi backend
CORS(app, origins=["https://thach-ai-frontend-fresh.vercel.app"])

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # <== kiểm tra đúng tên model
            messages=[
                {"role": "system", "content": "Bạn là trợ lý ảo ThamAI"},
                {"role": "user", "content": message}
            ]
        )
        reply = response['choices'][0]['message']['content']
        return jsonify({"response": reply})
    
    except Exception as e:
        print("❌ Lỗi khi gọi OpenAI:", e)  # In lỗi ra console
        return jsonify({"response": "⚠️ Đã xảy ra lỗi khi gọi OpenAI."})

    if not user_message:
        return jsonify({"response": "⚠️ Bạn chưa nhập tin nhắn nào cả."})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
		{"role": "system", "content":"Bạn là trợ lý ảo ThamAI"}, 
		{"role": "user", "content": message}
	    ]
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"response": reply})
    except Exception as e:
        print("❌ Lỗi gọi OpenAI:", e)
        return jsonify({"response": "⚠️ Đã xảy ra lỗi khi gọi OpenAI."})
        
# Khởi chạy ứng dụng Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

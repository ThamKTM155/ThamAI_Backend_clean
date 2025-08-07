from openai import OpenAI
from dotenv import load_dotenv
import os

# Nạp biến môi trường từ file .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Kiểm tra xem đã nạp được API key chưa
if not api_key:
    print("⚠️ Chưa tìm thấy biến OPENAI_API_KEY trong file .env.")
    exit()

# Tạo đối tượng client
client = OpenAI(api_key=api_key)

# Gửi yêu cầu đến OpenAI
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Bạn là trợ lý ảo ThamAI"},
            {"role": "user", "content": "Chào bạn"}
        ]
    )

    # In ra phản hồi
    print("✅ Phản hồi từ trợ lý ThamAI:\n", response.choices[0].message.content.strip())

except Exception as e:
    print("❌ Lỗi khi gọi OpenAI API:\n", e)

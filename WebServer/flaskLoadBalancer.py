from flask import Flask, redirect, request, jsonify
import requests
import random
import time

app = Flask(__name__)

# Danh sách các server Flask (có thể là các server chạy trên các cổng khác nhau)
SERVER_LIST = [
    'http://localhost:5001',
    'http://localhost:5002',
    'http://localhost:5003'
]

# Kiểm tra xem một server có hoạt động không
def is_server_alive(server):
    try:
        response = requests.get(f'{server}/health', timeout=3)  # Gửi yêu cầu GET để kiểm tra
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Lấy server Flask còn sống
def get_alive_server():
    # Kiểm tra từng server trong danh sách
    for server in SERVER_LIST:
        if is_server_alive(server):
            return server
    return None  # Trả về None nếu không có server nào hoạt động

@app.route('/')
def index():
    alive_server = get_alive_server()

    if alive_server:
        # Chuyển hướng đến server còn hoạt động
        return redirect(alive_server)
    else:
        return "Không có server nào hoạt động!", 503

# Đoạn endpoint này sẽ giúp kiểm tra sức khỏe của server
@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

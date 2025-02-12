from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from webApp.grpc_client import login, register, delete
import grpc

# Hàm xử lý yêu cầu đăng nhập
# Nhận dữ liệu từ request JSON, gọi hàm gRPC để xác thực người dùng
# Trả về phản hồi tương ứng dựa trên kết quả đăng nhập
def login_service():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Vui lòng điền đầy đủ thông tin!'}), 409

    username = data['username']
    password = data['password']

    try:
        status = login(username, password)

        if status == "Success":
            print("Login success")
            return jsonify({'message': f'Đăng nhập thành công cho {username}!'}), 200
        else:
            print(f"Login failed {status}")
            return jsonify({'message': 'Thông tin đăng nhập không chính xác!'}), 401

    except grpc.RpcError as e:
        error_detail = e.details() or "Lỗi gRPC không xác định"
        return jsonify({'message': f'Lỗi kết nối gRPC: {error_detail}'}), 500

# Hàm xử lý yêu cầu đăng ký tài khoản
# Nhận dữ liệu từ request JSON, gọi hàm gRPC để tạo tài khoản
# Kiểm tra xem tài khoản đã tồn tại chưa, trả về phản hồi tương ứng
def register_service():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Vui lòng điền đầy đủ thông tin!'}), 400

    username = data['username']
    password = data['password']

    try:
        status = register(username, password)

        if status == "Exist":  # Tài khoản đã tồn tại
            print("Register failed")
            return jsonify({'message': 'Tên người dùng đã tồn tại, vui lòng chọn tên khác!'}), 409
        if status == "Success":  # Đăng ký thành công
            print("Register success")
            return jsonify({'message': f'Đăng ký thành công cho {username}!'}), 201
        else:
            print(f"Register failed {status}")
            return jsonify({'message': 'Đăng ký thất bại, vui lòng thử lại!'}), 500

    except grpc.RpcError as e:
        error_detail = e.details() or "Lỗi gRPC không xác định"
        return jsonify({'message': f'Lỗi kết nối gRPC: {error_detail}'}), 500

# Hàm xử lý yêu cầu xóa người dùng
# Nhận dữ liệu từ request JSON, gọi hàm gRPC để xóa tài khoản
# Trả về phản hồi tương ứng dựa trên kết quả xóa
def delete_user_service():
    data = request.json
    if not data or 'username' not in data:
        return jsonify({'message': 'Vui lòng điền đầy đủ thông tin!'}), 400

    username = data['username']

    try:
        status = delete(username)

        if status == "Success":  # Xóa thành công
            print("Delete user success")
            return jsonify({'message': f'Xóa người dùng {username} thành công!'}), 200
        else:  # Xóa thất bại
            print(f"Delete user failed {status}")
            return jsonify({'message': 'Xóa người dùng thất bại, vui lòng thử lại!'}), 500

    except grpc.RpcError as e:
        error_detail = e.details() or "Lỗi gRPC không xác định"
        return jsonify({'message': f'Lỗi kết nối gRPC: {error_detail}'}), 500

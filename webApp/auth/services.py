from webApp.extension import db
from webApp.webstore_ma import UserSchema
from webApp.model import User, UserLocal
from flask import Flask, request, jsonify
from sqlalchemy.exc import IntegrityError
from webApp.grpc_client import login, register
import grpc

def login_service():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Vui lòng điền đầy đủ thông tin!'}), 409

    username = data['username']
    password = data['password']

    try:
        # Gọi gRPC để xác thực
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



def register_service():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Vui lòng điền đầy đủ thông tin!'}), 400

    username = data['username']
    password = data['password']

    try:
        status = register(username,password)

        if status == "Exist":
            print("Register failed")
            return jsonify({'message': 'Tên người dùng đã tồn tại, vui lòng chọn tên khác!'}), 409
        if status == "Success":
            print("Register success")
            return jsonify({'message': f'Đăng ký thành công cho {username}!'}), 201
        else:
            print(f"Register failed {status}")
            return jsonify({'message': 'Đăng ký thất bại, vui lòng thử lại!'}), 500

    except grpc.RpcError as e:
        error_detail = e.details() or "Lỗi gRPC không xác định"
        return jsonify({'message': f'Lỗi kết nối gRPC: {error_detail}'}), 500

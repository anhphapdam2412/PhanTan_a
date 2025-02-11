from flask import Blueprint, request, jsonify
from webApp.extension import db
from .services import login_service, register_service
from flask_cors import CORS
import traceback


auth= Blueprint('auth', __name__)
CORS(auth)

@auth.route('/login', methods=['POST'])
def login():
    return login_service()

@auth.route('/register', methods=['POST'])
def register():
    return register_service()

@auth.errorhandler(Exception)
def handle_exception(e):
    print("Lỗi không xác định:", str(e))
    print(traceback.format_exc())
    return jsonify({'message': f'Lỗi không xác định: {str(e)}'}), 500
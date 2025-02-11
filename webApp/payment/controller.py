from flask import Blueprint
from flask_cors import CORS
from .services import submit_payment_service

payment = Blueprint('payment', __name__)
CORS(payment)


@payment.route('/payment/submit', methods=['POST'])
def submit_payment():
    return submit_payment_service()

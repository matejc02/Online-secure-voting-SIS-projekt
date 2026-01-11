from flask import Blueprint, render_template
from services.authentication_service import jwt_required
from services.blockchain_service import calculate_winner

result_bp = Blueprint("result", __name__)


@result_bp.route('/results')
@jwt_required('ADMIN')
def get_show_results():
    message = calculate_winner()
    data = []
    if message['success']:
        data = message['votes']
    
    return render_template('results.html', data=data)

@result_bp.route('/winner')
@jwt_required()
def get_winner():
    message = calculate_winner()
    data = ""
    if message['success']:
        data = message['winner']
    
    return render_template('winner.html', data=data)

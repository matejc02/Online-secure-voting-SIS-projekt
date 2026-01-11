from flask import Blueprint, request, redirect, url_for, render_template
from services.voting_service import start_voting, stop_voting, is_voting_active, create_vote
from services.authentication_service import jwt_required
from services.candidate_service import get_all_candidates, get_candidate_by_id
from services.blockchain_service import calculate_winner
from services.user_service import delete_users_token, get_user_by_id

vote_bp = Blueprint("vote", __name__)

@vote_bp.route("/vote")
@jwt_required('VOTER')
def get_vote():
    data = []
    if is_voting_active():
        data = get_all_candidates()['data']
        return render_template('vote.html', candidates=data)

    message = calculate_winner()
    if message['success']:
        data.append(message['winner'])
        return render_template('vote.html', candidates=data)

    return render_template('vote.html', candidates=data)


@vote_bp.route('/vote/<int:id_candidate>', methods=["POST"])
@jwt_required('VOTER')
def post_vote(id_candidate):
    if is_voting_active():
        print(id_candidate)

        user_id = request.user['user_id']
        print(user_id)
        user = get_user_by_id(user_id)
        token = user.voting_token

        message = get_candidate_by_id(id_candidate)
        if message['success']:
            create_vote(message['candidate'], token)
            delete_users_token(user.id)

        return redirect(url_for('vote.get_vote'))

    return redirect(url_for('vote.get_vote'))


@vote_bp.route('/voting/start', methods=["POST"])
@jwt_required('ADMIN')
def start_voting_route():
    start_voting()
    return redirect(request.referrer)


@vote_bp.route('/voting/stop', methods=["POST"])
@jwt_required('ADMIN')
def stop_voting_route():
    stop_voting()
    return redirect(request.referrer)




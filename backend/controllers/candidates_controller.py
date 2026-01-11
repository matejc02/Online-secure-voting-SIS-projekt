from flask import Blueprint, request, redirect, url_for, render_template, abort
from services.candidate_service import create_candidate, get_all_candidates, delete_candidate_f
from services.authentication_service import jwt_required
from services.voting_service import is_voting_active


candidate_bp = Blueprint("candidate", __name__)

@candidate_bp.route('/candidates', methods=["GET", "POST"])
@jwt_required('ADMIN')
def get_post_candidates():
    if request.method == "POST":
        if is_voting_active():
            abort(403)

        username = request.form.get("name")
        email = request.form.get("email")
        description = request.form.get("description")

        print(" " + username + " " + email + " " + description)
        create_candidate(username, email, description)

        return redirect(url_for('candidate.get_post_candidates'))

    message = get_all_candidates()
    data = []
    if message["success"]:
        print(message['data'])
        data = message['data']
    else:
        print(message['message'])
    return render_template('candidates.html', candidates=data)


@candidate_bp.route('/deleteCandidate/<int:id_candidate>', methods=["POST"])
@jwt_required('ADMIN')
def delete_candidate(id_candidate):
    if is_voting_active():
        abort(403)
    
    delete_candidate_f(id_candidate)
    return redirect(url_for('candidate.get_post_candidates'))



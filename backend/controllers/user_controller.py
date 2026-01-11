from flask import Blueprint, request, redirect, url_for, render_template, abort
from services.authentication_service import jwt_required
from services.user_service import create_user, get_all_users, delete_user_f
from services.voting_service import is_voting_active

user_bp = Blueprint("user", __name__)


@user_bp.route('/allUsers', methods=["GET", "POST"])
@jwt_required('ADMIN')
def get_post_users():
    if request.method == "POST":
        username = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        print(" " + username + " " + email + " " + password)

        create_user(username, email, password)
        return redirect(url_for('user.get_post_users'))

    message = get_all_users()
    data = []
    if message["success"]:
        print(message['data'])
        data = message['data']
    else:
        print(message['message'])
    return render_template('users.html', users=data)


@user_bp.route('/deleteUser/<int:id_user>', methods=["POST"])
@jwt_required('ADMIN')
def delete_user(id_user):
    if is_voting_active():
        abort(403)
    delete_user_f(id_user)
    return redirect(url_for('user.get_post_users'))



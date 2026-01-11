from flask import Blueprint, request, redirect, url_for, make_response, render_template
from services.authentication_service import jwt_required, login_user, register_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def get_home_page():
    return render_template("home.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def get_post_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        print(" " + email + " " + password)

        message = login_user(email, password)

        if message['success'] == False:
            print(message['message'])
            return redirect(url_for('auth.get_home_page'))

        if message['user'].role == 'ADMIN':
            response = make_response(redirect(url_for('result.get_show_results')))
            jwt_token = message['token']
            response.set_cookie("access_token", jwt_token, httponly=True, secure=False)
            return response
        
        response = make_response(redirect(url_for('vote.get_vote')))
        jwt_token = message['token']
        response.set_cookie("access_token", jwt_token, httponly=True, secure=False)
        return response
    
    return render_template('login.html')


@auth_bp.route("/register", methods=["GET", "POST"])
def get_post_register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        print(" " + username + " " + email + " " + password)

        message = register_user(username, email, password)

        if message['message'] != "success":
            print(message['message'])
            return redirect(url_for('auth.get_home_page'))
        
        response = make_response(redirect(url_for('vote.get_vote')))
        jwt_token = message['token']
        response.set_cookie("access_token", jwt_token, httponly=True, secure=False)
        return response

    return render_template('register.html')


@auth_bp.route('/logout')
@jwt_required()
def logout():
    response = make_response(redirect(url_for('auth.get_home_page')))
    response.delete_cookie('access_token')
    return response


from flask import Flask, abort, render_template, redirect, url_for, flash, request, make_response
from functools import wraps
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta
from models import db
from services.authentication_service import jwt_required, login_user, register_user
from services.candidate_service import create_candidate, get_all_candidates, delete_candidate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'fjm034jhf0439uf423huj546890z2mf03j406h4v'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///online_shop.db"
app.config["JWT_SECRET_KEY"] = "hnf9weh809f208h9453207tgzh0f2bg208hj9321hrt"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def get_home_page():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def get_post_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        print(" " + email + " " + password)

        message = login_user(email, password)

        if message['success'] == False:
            print(message['message'])
            return redirect(url_for('get_home_page'))

        if message['user'].role == 'ADMIN':
            response = make_response(redirect(url_for('get_show_results')))
            jwt_token = message['token']
            response.set_cookie("access_token", jwt_token, httponly=True, secure=False)
            return response
        
        response = make_response(redirect(url_for('get_post_vote')))
        jwt_token = message['token']
        response.set_cookie("access_token", jwt_token, httponly=True, secure=False)
        return response
    
    return render_template('login.html')

@app.route("/register", methods=["GET", "POST"])
def get_post_register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        print(" " + username + " " + email + " " + password)

        message = register_user(username, email, password)

        if message['message'] != "success":
            print(message['message'])
            return redirect(url_for('get_home_page'))
        
        response = make_response(redirect(url_for('get_post_vote')))
        jwt_token = message['token']
        response.set_cookie("access_token", jwt_token, httponly=True, secure=False)
        return response

    return render_template('register.html')

@app.route('/vote', methods=["GET", "POST"])
@jwt_required('VOTER')
def get_post_vote():
    if request.method == "POST":
        pass

    return render_template('vote.html')

@app.route('/candidates', methods=["GET", "POST"])
@jwt_required('ADMIN')
def get_post_candidates():
    if request.method == "POST":
        username = request.form.get("name")
        email = request.form.get("email")
        description = request.form.get("description")

        print(" " + username + " " + email + " " + description)
        create_candidate(username, email, description)

        return redirect(url_for('get_post_candidates'))

    message = get_all_candidates()
    data = []
    if message["success"]:
        print(message['data'])
        data = message['data']
    else:
        print(message['message'])
    return render_template('candidates.html', candidates=data)

@app.route('/deleteCandidates/<int:id_candidate>', methods=["POST"])
@jwt_required('ADMIN')
def delete_candidates(id_candidate):
    delete_candidate(id_candidate)
    return redirect(url_for('get_post_candidates'))

@app.route('/allUsers', methods=["GET", "POST"])
@jwt_required('ADMIN')
def get_post_users():
    pass


@app.route('/refresh', methods=["GET", "POST"])
@jwt_required('ADMIN')
def get_post_refresh():
    pass

@app.route('/results')
@jwt_required('ADMIN')
def get_show_results():
    return "ADMIN ONLY !"

@app.route('/winner')
@jwt_required()
def get_winner():
    return "Ovdje ide html"

@app.route('/logout')
@jwt_required()
def logout():
    response = make_response(redirect(url_for('get_home_page')))
    response.delete_cookie('access_token')
    return response

if __name__ == "__main__":
    app.run(debug=True, port=5002)







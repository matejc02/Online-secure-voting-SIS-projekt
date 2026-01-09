from flask import Flask, abort, render_template, redirect, url_for, flash, request, make_response
from functools import wraps
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta
from models.models import db, VotingStatus
from services.authentication_service import jwt_required, login_user, register_user
from services.candidate_service import create_candidate, get_all_candidates, delete_candidate_f
from services.user_service import create_user, get_all_users, delete_user_f
from services.voting_service import start_voting, stop_voting, is_voting_active


app = Flask(__name__)
app.config['SECRET_KEY'] = 'fjm034jhf0439uf423huj546890z2mf03j406h4v'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///online_shop.db"
app.config["JWT_SECRET_KEY"] = "hnf9weh809f208h9453207tgzh0f2bg208hj9321hrt"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)

db.init_app(app)

with app.app_context():
    db.create_all()
    if not db.session.execute(db.select(VotingStatus)).scalar():
        db.session.add(VotingStatus(is_active=False))
        db.session.commit()

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
        
        response = make_response(redirect(url_for('get_vote')))
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

@app.route('/vote')
@jwt_required('VOTER')
def get_vote():
    data = []
    if is_voting_active():
        data = get_all_candidates()['data']
    
    return render_template('vote.html', candidates=data)

@app.route('/vote/<int:id_candidate>', methods=["POST"])
@jwt_required('VOTER')
def post_vote(id_candidate):
    if is_voting_active():
        print(id_candidate)
    
    return redirect(url_for('get_vote'))

@app.route('/candidates', methods=["GET", "POST"])
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

        return redirect(url_for('get_post_candidates'))

    message = get_all_candidates()
    data = []
    if message["success"]:
        print(message['data'])
        data = message['data']
    else:
        print(message['message'])
    return render_template('candidates.html', candidates=data)

@app.route('/deleteCandidate/<int:id_candidate>', methods=["POST"])
@jwt_required('ADMIN')
def delete_candidate(id_candidate):
    if is_voting_active():
        abort(403)
    delete_candidate_f(id_candidate)
    return redirect(url_for('get_post_candidates'))

@app.route('/allUsers', methods=["GET", "POST"])
@jwt_required('ADMIN')
def get_post_users():
    if request.method == "POST":
        username = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        print(" " + username + " " + email + " " + password)

        create_user(username, email, password)
        return redirect(url_for('get_post_users'))

    message = get_all_users()
    data = []
    if message["success"]:
        print(message['data'])
        data = message['data']
    else:
        print(message['message'])
    return render_template('users.html', users=data)

@app.route('/deleteUser/<int:id_user>', methods=["POST"])
@jwt_required('ADMIN')
def delete_user(id_user):
    if is_voting_active():
        abort(403)
    delete_user_f(id_user)
    return redirect(url_for('get_post_users'))

@app.route('/voting/start', methods=["POST"])
@jwt_required('ADMIN')
def start_voting_route():
    start_voting()
    return redirect(request.referrer)

@app.route('/voting/stop', methods=["POST"])
@jwt_required('ADMIN')
def stop_voting_route():
    stop_voting()
    return redirect(request.referrer)

@app.route('/refresh', methods=["GET", "POST"])
@jwt_required('ADMIN')
def get_post_refresh():
    pass

@app.route('/results')
@jwt_required('ADMIN')
def get_show_results():
    return render_template('results.html')

@app.route('/winner')
@jwt_required()
def get_winner():
    return render_template('winner.html')

@app.route('/logout')
@jwt_required()
def logout():
    response = make_response(redirect(url_for('get_home_page')))
    response.delete_cookie('access_token')
    return response

if __name__ == "__main__":
    app.run(debug=True, port=5002)







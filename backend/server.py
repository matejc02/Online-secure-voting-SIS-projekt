from flask import Flask, abort, render_template, redirect, url_for, flash, request, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Boolean, ForeignKey, Float, DateTime, and_
from functools import wraps
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fjm034jhf0439uf423huj546890z2mf03j406h4v'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///online_shop.db"
app.config["JWT_SECRET_KEY"] = "hnf9weh809f208h9453207tgzh0f2bg208hj9321hrt"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)

def jwt_required(role=None):
    def wrapper(function):
        @wraps(function)
        def check_jwt(*args, **kwargs):
            token = request.cookies.get('access_token')
            if not token:
                return abort(403)

            try:
                payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                return abort(401)
            except jwt.InvalidTokenError:
                return abort(401)

            if role and payload.get('role') != role:
                return abort(401)
            
            request.user = payload
            return function(*args, **kwargs)
        return check_jwt
    return wrapper

def create_jwt(user):
    token = jwt.encode(
        {'user_id': user.id, 'email': user.email, 'role': user.role, 'exp': datetime.utcnow() + app.config['JWT_ACCESS_TOKEN_EXPIRES']},
        app.config['JWT_SECRET_KEY'],
        algorithm="HS256"
    )

    return token

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(300), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(30), nullable=False)

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

        emails = [user.email for user in db.session.execute(db.select(User)).scalars().all()]
        if email not in emails:
            print("Email does not exists")
            return redirect(url_for('get_home_page'))

        user = db.session.execute(db.select(User).where(User.email == email)).scalar()

        if password == user.password:
            if user.role == 'ADMIN':
                response = make_response(redirect(url_for('get_show_results')))
                jwt_token = create_jwt(user)
                response.set_cookie("access_token", jwt_token, httponly=True, secure=False)
                return response
            
            response = make_response(redirect(url_for('get_post_vote')))
            jwt_token = create_jwt(user)
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

        emails = [user.email for user in db.session.execute(db.select(User)).scalars().all()]
        usernames = [user.username for user in db.session.execute(db.select(User)).scalars().all()]

        if email in emails:
            print("Email already exists")
            return redirect(url_for('get_home_page'))

        if username in usernames:
            print("Username already exists")
            return redirect(url_for('get_home_page'))

        new_User = User(
            username=username,
            email=email,
            password=password,
            role='VOTER'
        )
        
        db.session.add(new_User)
        db.session.commit()

        response = make_response(redirect(url_for('get_post_vote')))
        jwt_token = create_jwt(new_User)
        response.set_cookie("access_token", jwt_token, httponly=True, secure=False)

        return response

    return render_template('register.html')

@app.route('/vote', methods=["GET", "POST"])
@jwt_required('VOTER')
def get_post_vote():
    if request.method == "POST":
        pass

    return render_template('vote.html')

@app.route('/results')
@jwt_required('ADMIN')
def get_show_results():
    return "ADMIN ONLY !"

@app.route('/logout')
@jwt_required()
def logout():
    response = make_response(redirect(url_for('get_home_page')))
    response.delete_cookie('access_token')
    return response

if __name__ == "__main__":
    app.run(debug=True, port=5002)







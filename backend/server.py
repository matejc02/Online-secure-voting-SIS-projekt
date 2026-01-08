from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Boolean, ForeignKey, Float, DateTime, and_
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fjm034jhf0439uf423huj546890z2mf03j406h4v'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///online_shop.db"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

def admin_only(function):
    @wraps(function)
    def check_admin(*args, **kwargs):
        if current_user.role == 'ADMIN':
            return function(*args, **kwargs)
        return abort(403)
    
    return check_admin

def voter_only(function):
    @wraps(function)
    def check_voter(*args, **kwargs):
        if current_user.role == 'VOTER':
            return function(*args, **kwargs)
        return abort(403)
    
    return check_voter

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class User(UserMixin, Base):
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
            login_user(user)
            if user.role == 'ADMIN':
                return redirect(url_for('get_show_results'))    
            return redirect(url_for('get_post_vote'))
    
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

        login_user(new_User)

        return redirect(url_for('get_post_vote'))

    return render_template('register.html')

@app.route('/vote', methods=["GET", "POST"])
@login_required
@voter_only
def get_post_vote():
    if request.method == "POST":
        pass

    return render_template('vote.html')

@app.route('/results')
@login_required
@admin_only
def get_show_results():
    return "ADMIN ONLY !"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_home_page'))

if __name__ == "__main__":
    app.run(debug=True, port=5002)







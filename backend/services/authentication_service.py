from flask import request, abort
from functools import wraps
import jwt
from datetime import datetime
from flask import current_app
from models.models import db, User

def jwt_required(role=None):
    def wrapper(function):
        @wraps(function)
        def check_jwt(*args, **kwargs):
            token = request.cookies.get('access_token')
            if not token:
                return abort(403)

            try:
                payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
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
        {'user_id': user.id, 'email': user.email, 'role': user.role, 'exp': datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']},
        current_app.config['JWT_SECRET_KEY'],
        algorithm="HS256"
    )

    return token


def login_user(email, password):
    emails = [user.email for user in db.session.execute(db.select(User)).scalars().all()]

    if email not in emails:
        return {"success": False, "message": "Email does not exists"}
    
    user = db.session.execute(db.select(User).where(User.email == email)).scalar()

    if password == user.password:
        jwt_token = create_jwt(user)
        return {"success": True, "message": "success", "token": jwt_token, "user": user}
        
    return {"success": False, "message": "Wrong password"}


def register_user(username, email, password):
    emails = [user.email for user in db.session.execute(db.select(User)).scalars().all()]
    usernames = [user.username for user in db.session.execute(db.select(User)).scalars().all()]

    if email in emails or email == "":
        print("Email already exists")
        return {"success": False, "message": "Email already exists"}
    
    if username in usernames or username == "":
        return {"success": False, "message": "Username already exists"}
    
    new_User = User(
        username=username,
        email=email,
        password=password,
        role='VOTER'
    )
    
    db.session.add(new_User)
    db.session.commit()
    
    jwt_token = create_jwt(new_User)
    
    return {"success": True, "message": "success", "token": jwt_token}



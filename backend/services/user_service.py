from flask import request, abort
from datetime import datetime
from flask import current_app
from models.models import db, User
import secrets
from werkzeug.security import generate_password_hash, check_password_hash

def create_admin():
    roles = [user.role for user in db.session.execute(db.select(User)).scalars().all()]
    user = db.session.execute(db.select(User).where(User.id == 0)).scalar()
    if 'ADMIN' not in roles and user == None:
        new_user = User(
            id=0,
            username='admin',
            email='admin@email.com',
            password=generate_password_hash("12345", method='pbkdf2:sha256', salt_length=8),
            role='ADMIN'
        )

        db.session.add(new_user)
        db.session.commit()

def create_user(username, email, password):
    usernames = [user.username for user in db.session.execute(db.select(User)).scalars().all()]
    emails = [user.email for user in db.session.execute(db.select(User)).scalars().all()]

    if username in usernames or username == "":
        return {"success": False, "message": "That name already exists !"}
    
    if email in emails or email == "":
        return {"success": False, "message": "That email username already exists"}

    new_user = User(
        username=username,
        email=email,
        password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8),
        role='VOTER',
        voting_token=secrets.token_hex(16)
    )

    db.session.add(new_user)
    db.session.commit()

    return {"success": True, "message": "User successfully added"}

def get_all_users():
    all_users = [user for user in db.session.execute(db.select(User)).scalars().all()]

    if all_users:
        return {"success": True, "data": all_users}
    
    return {"success": False, "message": "There are no users"}


def delete_user_f(id_user):
    db.session.delete(db.session.execute(db.select(User).where(User.id == id_user)).scalar())
    db.session.commit()

    return {"success": True}


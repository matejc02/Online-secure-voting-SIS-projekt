from flask import request, abort
from datetime import datetime
from flask import current_app
from models.models import db, User

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
        password=password,
        role='VOTER'
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


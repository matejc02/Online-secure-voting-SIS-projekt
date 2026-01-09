from flask import request, abort
from datetime import datetime
from flask import current_app
from models import db, Candidate

def create_candidate(username, email, description):
    usernames = [user.fullname for user in db.session.execute(db.select(Candidate)).scalars().all()]
    emails = [user.email for user in db.session.execute(db.select(Candidate)).scalars().all()]

    if username in usernames:
        return {"message": "That name already exists !"}

    if email in emails:
        return {"message": "That email already exists !"}

    new_candidate = Candidate(
        fullname=username,
        email=email,
        description=description
    )

    db.session.add(new_candidate)
    db.session.commit()

    return {"message": "success"}

def get_all_candidates():
    all_candidates = [candidate for candidate in db.session.execute(db.select(Candidate)).scalars().all()]

    if all_candidates:
        return {"success": True, "data": all_candidates}

    return {"success": False, "message": "There are no candidates"}

def get_current_winner():
    pass

def delete_candidate(id_candidate):
    db.session.delete(db.session.execute(db.select(Candidate).where(Candidate.id == id_candidate)).scalar())
    db.session.commit()

    return {"success": True}


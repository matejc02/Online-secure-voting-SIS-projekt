from models.models import User, UsedTokens
from extensions import db
import secrets
from werkzeug.security import generate_password_hash
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

def create_admin():
    roles = [user.role for user in db.session.execute(db.select(User)).scalars().all()]
    user = db.session.execute(db.select(User).where(User.id == 0)).scalar()
    if 'ADMIN' not in roles and user == None:
        new_user = User(
            id=0,
            username='admin',
            email='admin@email.com',
            password=generate_password_hash("12345", method='pbkdf2:sha256', salt_length=8),
            role='ADMIN',
            public_key='dfh92904hg974g2t97'
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

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode("utf-8")

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode("utf-8")

    new_user = User(
        username=username,
        email=email,
        password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8),
        role='VOTER',
        voting_token=secrets.token_hex(16),
        public_key=public_pem,
        private_key=private_pem
    )

    db.session.add(new_user)
    db.session.commit()

    return {"success": True, "message": "User successfully added"}

def get_all_users():
    all_users = [user for user in db.session.execute(db.select(User)).scalars().all()]

    if all_users:
        return {"success": True, "data": all_users}
    
    return {"success": False, "message": "There are no users"}

def get_user_by_id(id):
    user = db.session.execute(db.select(User).where(User.id == id)).scalar()
    
    return user

def delete_user_f(id_user):
    db.session.delete(db.session.execute(db.select(User).where(User.id == id_user)).scalar())
    db.session.commit()

    return {"success": True}

def get_used_tokens():
    tokens = [used_token.token for used_token in db.session.execute(db.select(UsedTokens)).scalars().all()]
    return tokens


def delete_users_token(id):
    user = db.session.execute(db.select(User).where(User.id == id)).scalar()

    if not user:
        return {"success": False, "message": "User not found"}
    
    user.voting_token = None
    db.session.commit()

    return {"success": True, "message": "Voting token deleted"}

def set_token_to_all_users():
    users = [user for user in db.session.execute(db.select(User)).scalars().all()]

    for user in users:
        if user.voting_token is None:
            user.voting_token = secrets.token_hex(16)
            db.session.commit()

    return {"success": True}



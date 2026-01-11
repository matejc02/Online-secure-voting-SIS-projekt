from models.models import VotingStatus, UsedTokens
from extensions import db
from services.user_service import set_token_to_all_users, get_used_tokens
from services.json_service import delete_all, create_genesis_block
from services.blockchain_service import create_commitment, create_zkp, create_block, create_vote_message, sign_vote
import time
from cryptography.hazmat.primitives import serialization

def is_voting_active():
    status = db.session.execute(
        db.select(VotingStatus)
    ).scalar()
    return status.is_active

def delete_all_used_tokens():
    db.session.query(UsedTokens).delete()
    db.session.commit()

def start_voting():
    status = db.session.execute(db.select(VotingStatus)).scalar()
    if status.is_active == False:
        status.is_active = True
        db.session.commit()
        delete_all()
        create_genesis_block()
        set_token_to_all_users()
        delete_all_used_tokens()

def stop_voting():
    status = db.session.execute(db.select(VotingStatus)).scalar()
    if status.is_active == True:
        status.is_active = False
        db.session.commit()

def create_vote(candidate, user_token, user):
    id = candidate.id
    name = candidate.fullname
    timestamp = time.time()

    used_tokens = get_used_tokens()
    if user_token in used_tokens or user_token == None:
        print("Vote already exists !")
        return

    commitment, secret = create_commitment(name)
    zkp = create_zkp(commitment, secret)

    message = create_vote_message(commitment, user_token, zkp)

    private_key = serialization.load_pem_private_key(
        user.private_key.encode("utf-8"),
        password=None
    )

    public_key = serialization.load_pem_public_key(
        user.public_key.encode("utf-8")
    )

    signature = sign_vote(private_key, message)

    create_block(commitment, user_token, zkp, secret, id, timestamp, signature, public_key)


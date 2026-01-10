import secrets
import hashlib
from models.block import Block
from services.json_service import add_block, get_all_blocks
from services.candidate_service import get_all_candidates
from services.user_service import get_used_tokens

def create_commitment(candidate_name):
    secret = secrets.token_hex(16)

    commitment = hashlib.sha256(
        (candidate_name + secret).encode()
    ).hexdigest()

    return commitment, secret

def create_zkp(commitment, secret):
    return hashlib.sha256(
        (commitment + secret).encode()
    ).hexdigest()

def verify_zkp(commitment, secret, zkp):
    calculate = hashlib.sha256(
        (commitment + secret).encode()
    ).hexdigest()
    return calculate == zkp

def calculate_hash(previousHash, token_commitment, commitment, zkp, encrypted_vote, timestamp):
    data = str(previousHash) + commitment + zkp + str(timestamp) + str(encrypted_vote) + token_commitment
    return hashlib.sha256(data.encode()).hexdigest()

def get_previous_block_hashes():
    all_blocks = get_all_blocks()
    return all_blocks[-1]["blockHash"]

def create_block(commitment, token_commitment, zkp, secret, vote, timestamp):
    if not verify_zkp(commitment, secret, zkp):
        print("Invalid ZKP - vote rejected")
        return
        
    used_tokens = get_used_tokens()

    if token_commitment in used_tokens:
        print("Vote already exists")
        return

    previousHash = get_previous_block_hashes()
    blockHash = calculate_hash(previousHash, commitment, token_commitment, zkp, vote, timestamp)

    newBlock = Block(
        previousHash,
        commitment,
        token_commitment,
        zkp,
        vote,
        timestamp,
        blockHash
    )

    add_block(newBlock)

def calculate_winner():
    message = get_all_candidates()

    if not message['success']:
        return {"success": False, "message": "There are no candidates"}

    candidates = message['data']

    vote_count = {}
    for candidate in candidates:
        vote_count[int(candidate.id)] = 0

    all_blocks = get_all_blocks()

    if not all_blocks or len(all_blocks) <= 1:
        return {"success": False, "message": "There are no votes"}

    for block in all_blocks[1:]:
        vote = int(block['encrypted_vote'])
        if vote in vote_count:
            vote_count[vote] += 1

    winner_id = max(vote_count, key=vote_count.get)

    winner_candidate = next(
        (candidate for candidate in candidates if int(candidate.id) == winner_id),
        None
    )

    return {
        "success": True,
        "winner": winner_candidate,
        "votes": vote_count
    }


def show_blockchain_results():
    pass


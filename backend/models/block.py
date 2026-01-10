class Block:
    def __init__(self, previousBlockHash, commitment, token_commitment, zkp, encrypted_vote, timestamp, blockHash):
        self.previousBlockHash = previousBlockHash
        self.commitment = commitment
        self.token_commitment = token_commitment
        self.zkp = zkp
        self.encrypted_vote = encrypted_vote
        self.timestamp = timestamp
        self.blockHash = blockHash

    def get_token_commitment(self):
        return self.token_commitment

    def get_previous_hash(self):
        return self.previousBlockHash
    
    def get_blockHash(self):
        return self.blockHash

    def get_commitment(self):
        return self.commitment
    
    def get_zkp(self):
        return self.zkp
    
    def get_vote(self):
        return self.encrypted_vote

    def get_timestamp(self):
        return self.timestamp




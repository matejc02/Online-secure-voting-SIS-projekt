import json

def create_genesis_block():
    with open("resources/blockchain.json", "r") as f:
        data = json.load(f)

    if data == []:
        data.append({
            "previousBlockHash": 0,
            "commitment": 0,
            "token_commitment": 0,
            "zkp": 0,
            "encrypted_vote": 0,
            "timestamp": 0,
            "blockHash": 0
        })

        with open("resources/blockchain.json", "w") as f:
            json.dump(data, f, indent=4)

def add_block(block):
    with open("resources/blockchain.json", "r") as f:
        data = json.load(f)

    data.append({
        "previousBlockHash": block.get_previous_hash(),
        "commitment": block.get_commitment(),
        "token_commitment": block.get_token_commitment(),
        "zkp": block.get_zkp(),
        "encrypted_vote": block.get_vote(),
        "timestamp": block.get_timestamp(),
        "blockHash": block.get_blockHash()
    })

    with open("resources/blockchain.json", "w") as f:
        json.dump(data, f, indent=4)

def get_all_blocks():
    with open("resources/blockchain.json", "r") as f:
        data = json.load(f)
    
    return data

def delete_all():
    with open("resources/blockchain.json", "w") as f:
        json.dump([], f)



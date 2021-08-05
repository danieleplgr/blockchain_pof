import json, time

from backend.util.hashing import get_block_hash
from backend.util.hexbinary import hex_to_binary
from backend.config import MINE_RATE


GENESIS_DATA = {
    "timestamp": 1,
    "hash": "genesis_hash",
    "last_hash": "",
    "data": [{"id": "aaaaaaaa", "input": {"address": None}, "output": {}}], 
    "difficulty": 3,
    "nonce": "test"
}


class Block:
    """
    Block: Represents a sigle block of data for the blockchain.
    """
    def __init__(self, timestamp: int, hash: str, last_hash: str, data: object, difficulty: int, nonce: int):
        self.timestamp = timestamp
        self.data = data
        self.hash = hash
        self.last_hash = last_hash
        self.difficulty = difficulty
        self.nonce = nonce
    

    def __repr__(self): 
        return (
            f"{{Block: timestamp:{json.dumps(self.timestamp)}, "
            f"difficulty:{json.dumps(self.difficulty)}, nonce:{json.dumps(self.nonce)}, "   
            f"data:{json.dumps(self.data)}, hash:{self.hash}, last_hash:{self.last_hash}}}"
        )
    

    @staticmethod
    def mine_block(last_block, data: object):
        """
        Mine the "next" block based on last_block and data of the current block data untill a valid hash 
        (with leading zero corresponding to difficulty) is found
        """
        nonce = 0
        timestamp = time.time_ns()
        difficulty = Block.adjust_difficulty(last_block, timestamp)
        last_block_hash = last_block.hash
        hash = get_block_hash(timestamp, last_block_hash, data, difficulty, nonce)
        hex_binary_hash = hex_to_binary(hash)

        while hex_binary_hash[0:difficulty] != '0'*difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            hash = get_block_hash(timestamp, last_block_hash, data, difficulty, nonce)
            hex_binary_hash = hex_to_binary(hash)

        return Block(timestamp, hash, last_block_hash, data, difficulty, nonce)
    

    @staticmethod
    def genesis():
        """
        Create the first genesis block
        """ 
        return Block(**GENESIS_DATA)

    
    @staticmethod
    def adjust_difficulty(last_block, current_block_timestamp_ns: int):
        """
        Calculate the adjusted difficulty based on last block generation time and expected MINE_RATE.
        Increase difficulty if blocks are mined too fast otherwise decrement
        """
        last_block_mining_ns = current_block_timestamp_ns - last_block.timestamp 
        if (last_block_mining_ns < MINE_RATE):
            return last_block.difficulty +1
        
        elif (last_block_mining_ns > MINE_RATE):
            if (last_block.difficulty -1) > 0:
                return last_block.difficulty -1
            return 1
        
        else:
            return last_block.difficulty


    @staticmethod
    def is_valid_block(last_block, block):
        """
        Validating the block using followuing rules:
        - Verify that the last_block hash is present in the mined block 
        - Re-calculate and verify the mined block hash using the mined_block fields
        - Verify the "proof-of-work" requirements (difficulty) in the hash of the mined block
        - Difficuly must be adjusted only by 1
        """
        if last_block.hash != block.last_hash:
            raise Exception("last_block hash and mined block last_hash must be identical")
        
        if hex_to_binary(block.hash)[0:block.difficulty] != '0'*block.difficulty:
            raise Exception("Proof-of-work requirements not met")
        
        if abs(last_block.difficulty - block.difficulty) != 1:
            raise Exception("Block difficulty can be adjusted only by 1 unit")
        
        recostructed_hash = get_block_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.difficulty,
            block.nonce
        )
        if recostructed_hash != block.hash:
            raise Exception("Wrong hash re-calculation from args: potential security risk avoided")
    

    @staticmethod
    def from_json(block_json):
        """
        Deserialize from json
        """
        return Block(**block_json)

    
    def __eq__(self, other: object):
        return self.__dict__ == other.__dict__
    

    def to_json(self):
        """
        Returns a valid json serializable object
        """
        repr = self.__dict__
        #repr['bin_hash'] = hex_to_binary(self.hash)
        return repr
    

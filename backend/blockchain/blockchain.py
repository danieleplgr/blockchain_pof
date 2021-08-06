import json
from backend.blockchain.block import Block, GENESIS_BLOCK_HASH
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD_INPUT, MINING_REWARD_FROM_ADDRESS


class Blockchain:
    """
    Blockchain: it's a chain of Blocks linked using the last_hash of each one referring the hash of the previuos Block.
    Implemented using a list
    """

    def __init__(self):
        genesis_block = Block.genesis()
        self.chain = [genesis_block]
    

    def add_block(self, data: object):
        """
        Adds the data to the blockchain as last Block 
        """
        last_block = self.chain[-1]
        self.chain.append(Block.mine_block(last_block, data))


    def replace_chain(self, chain: list):
        """
        Replace the chain with the new one if following occurs:
        - the new one must be longer
        - the incoming chain is valid 
        """
        if len(chain) <= len(self.chain):
            raise Exception("Cannot replace chain, new one must be longer")

        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f"Cannot replace chain, incoming chain is invalid: {e}")
        
        self.chain = chain


    def to_json(self):
        """
        Returns the a valid serializable json object
        """
        return list(map(lambda block: block.to_json(), self.chain))


    @staticmethod
    def is_valid_chain(chain: list):
        """
        validate all the passed chain using those rules
        - chain must start with genesis block
        - blocks must be formatted correctly  
        """
        if chain[0] != Block.genesis():
            raise Exception("Genesis block must be valid")

        # blocks validation
        for i in range(1, len(chain)-1):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, block)
        
        # transactions validation
        Blockchain.are_valid_transactions_in_chain(chain)

    

    @staticmethod
    def are_valid_transactions_in_chain(chain: list):
        """
        Enforce the rules of validation for the transactions in the block-chain
        - only 1 mining reward transaction
        - only 1 unique identified transaction can exists in the blockchain
        - each transaction must be valid 
        """
        transactions_ids = set()

        for i in range(len(chain)):
            block = chain[i]

            if block.hash != GENESIS_BLOCK_HASH: 
                has_mining_reward = False

                for transaction_dict in block.data: 
                    transaction = Transaction.from_json(transaction_dict)
                    
                    # unique transaction check
                    if transaction.id in transactions_ids:
                        raise Exception(f"Duplicated transaction with id:{transaction.id}")
                    transactions_ids.add(transaction.id)

                    # check 1 mining reward
                    if transaction.input == MINING_REWARD_INPUT:
                        if has_mining_reward:
                            raise Exception(f"Multiple mining rewards in block: {block.hash}")
                        has_mining_reward = True

                    # check transaction validity
                    Transaction.is_valid_transaction(transaction)

                    # check the balance is correct through the blockchain blocks (skip reward miner wallet address)
                    if transaction.input['address'] != MINING_REWARD_FROM_ADDRESS:
                        historic_blockchain = Blockchain() 
                        historic_blockchain.chain = chain[0:i]
                        historic_balance = Wallet.calculate_balance(historic_blockchain, transaction.input['address'])
                        if transaction.input['address'] != MINING_REWARD_FROM_ADDRESS:
                            if historic_balance != transaction.input['amount']:
                                raise Exception(f"Invalid input transaction amount not equals historic balance \
                                    amount for transaction.id {transaction.id}")

                if not has_mining_reward:
                    raise Exception(f"No mining reward found in block: {block.hash}")




    @staticmethod
    def from_json(json_blockchain: list):
        """
        Deserialize a list of blocks into a Blockchain instances, containing a list of Block instances
        """
        blockchain = Blockchain()
        blockchain.chain = list(map(lambda dict_block: Block.from_json(dict_block) ,json_blockchain))
        return blockchain
        

    def __repr__(self): 
        return f"Blockchain: {self.chain}"


if __name__ == '__main__':
    blockchain = Blockchain() 
    block_data = "1th_block_data"
    blockchain.add_block(block_data)
    blockchain.add_block("2th_block_data")
    print(blockchain)
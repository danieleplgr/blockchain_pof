import pytest
from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA, Block
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction



@pytest.fixture
def blockchain_3_blocks():
    blockchain = Blockchain()
    for i in range(3):  
        reward_transaction = Transaction.create_reward_transaction(Wallet()).to_json() 
        transactions_as_dicts = [ Transaction(Wallet(), "recipient", i+10).to_json() ]
        transactions_as_dicts.append(reward_transaction) 
        blockchain.add_block( transactions_as_dicts )
    return blockchain



def test_blockchain_instance():
    blockchain = Blockchain()
    blockchain.chain[0].data == GENESIS_DATA['data']


def test_add_block():
    blockchain = Blockchain()
    data = "data_2th_block"
    blockchain.add_block(data)
    blockchain.chain[-1].data == data


def test_is_valid_chain(blockchain_3_blocks):
    Blockchain.is_valid_chain(blockchain_3_blocks.chain)


def test_is_valid_chain_bad_genesis(blockchain_3_blocks):
    blockchain_3_blocks.chain[0] = Block.genesis()
    blockchain_3_blocks.chain[0].difficulty = blockchain_3_blocks.chain[0].difficulty+1
    with pytest.raises(Exception):
        Blockchain.is_valid_chain(blockchain_3_blocks.chain)


def test_replace_chain(blockchain_3_blocks):
    blockchain = Blockchain()
    blockchain.replace_chain(blockchain_3_blocks.chain)
    assert blockchain_3_blocks.chain == blockchain.chain


def test_replace_chain_incoming_smaller(blockchain_3_blocks):
    blockchain = Blockchain()
    with pytest.raises(Exception):
        blockchain_3_blocks.replace_chain(blockchain.chain) 
    assert blockchain_3_blocks.chain != blockchain.chain


def test_replace_chain_invalid_incoming_chain(blockchain_3_blocks):
    blockchain = Blockchain()
    blockchain_3_blocks.chain[1] = "evil_hash"
    with pytest.raises(Exception, match="incoming chain is invalid"):
        blockchain.replace_chain(blockchain_3_blocks.chain) 


def test_isvalid_transactions_in_chain(blockchain_3_blocks):
    Blockchain.are_valid_transactions_in_chain(blockchain_3_blocks.chain)


def test_isvalid_transactions_in_chain_duplicated_transaction(blockchain_3_blocks):
    transaction = Transaction(Wallet(), "recipient_d", 11).to_json()
    reward_transaction = Transaction.create_reward_transaction(Wallet()).to_json() 
    blockchain_3_blocks.add_block( [transaction, transaction, reward_transaction] )
    with pytest.raises(Exception, match="Duplicated transaction"):
        Blockchain.are_valid_transactions_in_chain(blockchain_3_blocks.chain)


def test_isvalid_transactions_in_chain_multiple_rewards(blockchain_3_blocks):
    transaction = Transaction(Wallet(), "recipient_d", 11).to_json()
    reward_transaction_1 = Transaction.create_reward_transaction(Wallet()).to_json() 
    reward_transaction_2 = Transaction.create_reward_transaction(Wallet()).to_json()  
    blockchain_3_blocks.add_block( [transaction, reward_transaction_1, reward_transaction_2] )
    with pytest.raises(Exception, match="Multiple mining rewards in block"):
        Blockchain.are_valid_transactions_in_chain(blockchain_3_blocks.chain)


def test_isvalid_transactions_in_chain_bad_transaction(blockchain_3_blocks):
    bad_transaction = Transaction(Wallet(), "recipient", 111)
    bad_transaction.input['signature'] = Wallet().sign(bad_transaction.output)
    blockchain_3_blocks.add_block( [bad_transaction.to_json() ] )
    with pytest.raises(Exception ):
        Blockchain.are_valid_transactions_in_chain(blockchain_3_blocks.chain)


def test_isvalid_transactions_in_chain_bad_historic_balance(blockchain_3_blocks):
    sender_wallet = Wallet()
    bad_transaction = Transaction(sender_wallet, "recipient", 1)
    bad_transaction.output[sender_wallet.address] = 9000
    bad_transaction.input['amount'] = 9001
    bad_transaction.input['signature'] = sender_wallet.sign(bad_transaction.output)
    #reward_transaction = Transaction.create_reward_transaction(Wallet()) 

    blockchain_3_blocks.add_block( [bad_transaction.to_json() ] )
    with pytest.raises(Exception, match="Invalid input transaction amount not equals historic balance" ):
        Blockchain.are_valid_transactions_in_chain(blockchain_3_blocks.chain)
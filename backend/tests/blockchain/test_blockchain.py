import pytest
from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA, Block


def test_blockchain_instance():
    blockchain = Blockchain()
    blockchain.chain[0].data == GENESIS_DATA['data']


def test_add_block():
    blockchain = Blockchain()
    data = "data_2th_block"
    blockchain.add_block(data)
    blockchain.chain[-1].data == data


@pytest.fixture
def blockchain_3_blocks():
    blockchain = Blockchain()
    for i in range(4):
        blockchain.add_block("data"+str(i))
    return blockchain


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
import time, pytest
from backend.config import MINE_RATE, SECS
from backend.blockchain.block import Block, GENESIS_DATA
from backend.util.hexbinary import hex_to_binary


def test_mine_block():
    last_block = Block.genesis()
    actual_data = "my_data 123"
    actual_block = Block.mine_block(last_block, actual_data)
    assert isinstance(actual_block, Block)
    assert actual_block.data == actual_data
    assert actual_block.last_hash == last_block.hash
    assert hex_to_binary(actual_block.hash)[0:actual_block.difficulty] == '0'*actual_block.difficulty


def test_genesis_block():
    genesis_block = Block.genesis()
    assert isinstance(genesis_block, Block) 
    assert genesis_block.data == GENESIS_DATA['data']
    assert genesis_block.timestamp == GENESIS_DATA['timestamp']
    assert genesis_block.last_hash == GENESIS_DATA['last_hash']


def test_block_mined_increase_difficulty():
    """
    Check we want to increase difficulty in case blocks are mined too quickly
    In the 1th block from genesis we surely have to increase difficulty.
    """
    last_block = Block.mine_block(Block.genesis(), "foo")
    current_block = Block.mine_block(last_block, "bar")
    assert current_block.difficulty == (last_block.difficulty +1)


def test_block_mined_decrease_difficulty():
    """
    Check we want to decrease difficulty in case blocks are mined too slowly.
    """
    last_block = Block.mine_block(Block.genesis(), "foo")
    time.sleep( MINE_RATE / SECS )
    mined_block = Block.mine_block(last_block, "bar")
    assert mined_block.difficulty == (last_block.difficulty -1)


def test_mine_block_difficulty_limit_one():
    """
    Check we want to have as minimum decreased difficulty = 1, never lower than 1
    """
    last_block = Block(
        time.time_ns(), 
        "hash",
        "last_hash",
        "last_data",
        1,
        0
    )
    time.sleep( MINE_RATE / SECS )
    mined_block = Block.mine_block(last_block, "bar")
    assert mined_block.difficulty == 1


@pytest.fixture
def last_block():
    return Block.genesis()

@pytest.fixture
def block(last_block):
    return Block.mine_block(last_block, "data")


def test_is_valid_block(last_block, block): 
    Block.is_valid_block(last_block, block)


def test_is_valid_block_bad_last_hash(last_block, block): 
    block.last_hash = "evil_last_hash"
    with pytest.raises(Exception):
        Block.is_valid_block(last_block, block)


def test_is_valid_block_bad_proof_of_work(last_block, block): 
    block.hash = "abcd123456789"
    with pytest.raises(Exception):
        Block.is_valid_block(last_block, block)


def test_is_valid_block_jumped_difficulty(last_block, block): 
    block.difficulty = last_block.difficulty +10
    block.hash = f"{'0'*block.difficulty}123456"
    with pytest.raises(Exception):
        Block.is_valid_block(last_block, block)


def test_is_valid_block_bad_block_hash(last_block, block): 
    block.hash = "000000000031cdcfd06d2eaca03501bf17a2fc633fb578cddd4c5daf3ce2fc1d"
    with pytest.raises(Exception):
        Block.is_valid_block(last_block, block)

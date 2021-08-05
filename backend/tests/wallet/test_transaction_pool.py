from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.wallet import Wallet
from backend.blockchain.blockchain import Blockchain


def test_set_transaction():
    transaction_pool = TransactionPool()
    transaction = Transaction(Wallet(), "recipient", 1)
    transaction_pool.set_transaction(transaction)
    print(f"transaction.id {transaction.id} ")
    assert transaction_pool.transaction_map[transaction.id] == transaction 


def test_clear_inblockchain_transactions():
    transaction_pool = TransactionPool()
    transaction_1 = Transaction(Wallet(), "recipient", 1)
    transaction_2 = Transaction(Wallet(), "recipient", 2)
    transaction_pool.set_transaction(transaction_1)
    transaction_pool.set_transaction(transaction_2)

    blockchain = Blockchain()
    blockchain.add_block( [transaction_1.to_json(), transaction_2.to_json()] ) 
    assert len(blockchain.chain) == 2
    assert transaction_1.id in transaction_pool.transaction_map
    assert transaction_2.id in transaction_pool.transaction_map
    transaction_pool.clear_blockchain_transactions(blockchain)
    assert transaction_1.id not in transaction_pool.transaction_map
    assert transaction_2.id not in transaction_pool.transaction_map
    assert len(transaction_pool.transaction_map.keys()) == 0
    assert len(blockchain.chain) == 2

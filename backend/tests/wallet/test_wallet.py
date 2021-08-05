from backend.wallet.wallet import Wallet
from backend.blockchain.blockchain import Blockchain
from backend.config import STARTING_BALANCE
from backend.wallet.transaction import Transaction


def test_verify_valid_signature():
    data = {"foo": "bar"}
    wallet = Wallet()
    signature = wallet.sign(data)
    assert wallet.verify_signature(wallet.public_key, data, signature)


def test_verify_invalid_signature():
    data = {"foo": "bar"}
    wallet = Wallet()
    signature = wallet.sign(data)
    other_public_key = Wallet().public_key
    assert not wallet.verify_signature(other_public_key, data, signature)


def test_calculate_balance():
    # starting balance
    blockchain = Blockchain()
    wallet = Wallet()
    assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE

    # sender balance test
    amount = 50
    transaction = Transaction(wallet, "recipient", amount)
    blockchain.add_block([transaction.to_json()])
    assert Wallet.calculate_balance(blockchain, wallet.address) == \
        STARTING_BALANCE - amount

    # recipient balance test
    received_amount_1 = 25
    received_transaction_1 = Transaction(
        Wallet(), wallet.address, received_amount_1, 
    )

    received_amount_2 = 11
    received_transaction_2 = Transaction(
        Wallet(), wallet.address, received_amount_2, 
    )
    blockchain.add_block([received_transaction_1.to_json(), \
        received_transaction_2.to_json()])
    
    assert Wallet.calculate_balance(blockchain, wallet.address) == \
        (STARTING_BALANCE - amount + received_amount_1 + received_amount_2)

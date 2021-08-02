import pytest
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet


def test_transaction():
    sender_wallet = Wallet()
    recipient_address = "aaaabbbb"
    amount = 50
    transaction = Transaction(sender_wallet, recipient_address, amount)
    assert transaction.output[recipient_address] == amount
    assert transaction.output[sender_wallet.address] == (sender_wallet.balance - amount)
    assert "timestamp" in transaction.input
    assert  transaction.input["amount"] == sender_wallet.balance
    assert  transaction.input["address"] == sender_wallet.address
    assert  transaction.input["public_key"] == sender_wallet.public_key
    Wallet.verify_signature(sender_wallet.public_key, transaction.output, transaction.input["signature"])



def test_transaction_exceed_balance():
    with pytest.raises(Exception, match="amount exceed the balance"):
        sender_wallet = Wallet()
        sender_wallet.balance = 10
        recipient_address = "aaaabbbb"
        amount = 50 
        Transaction(sender_wallet, recipient_address, amount)



def test_transaction_update(): 
    sender_wallet = Wallet()
    sender_wallet.balance = 60
    recipient_address = "aaaabbbb"
    next_recipient = "ccccdddd"
    amount = 50 
    next_amount = 10
    t1 = Transaction(sender_wallet, recipient_address, amount)
    t1.update(sender_wallet, next_recipient, next_amount)

    assert t1.output[recipient_address] == amount
    assert t1.output[next_recipient] == next_amount
    assert t1.output[sender_wallet.address] == 0
    assert Wallet.verify_signature(sender_wallet.public_key, t1.output, t1.input["signature"])



def test_transaction_update_exceed_balance():
    with pytest.raises(Exception, match="amount exceed the balance"):
        sender_wallet = Wallet()
        sender_wallet.balance = 55
        recipient_address = "aaaabbbb"
        amount = 50 
        t1 = Transaction(sender_wallet, recipient_address, amount)
        t1.update(sender_wallet, "ccccdddd", 10)



def test_valid_transaction():
    sender_wallet = Wallet()
    recipient_address = "aaaabbbb"
    amount = 50
    transaction = Transaction(sender_wallet, recipient_address, amount)
    Transaction.is_valid_transaction(transaction)


def test_valid_transaction_with_invalid_output():
    sender_wallet = Wallet()
    recipient_address = "aaaabbbb"
    amount = 50
    transaction = Transaction(sender_wallet, recipient_address, amount)
    transaction.output[sender_wallet.address] = 9990
    with pytest.raises(Exception, match="Invalid transaction output values"):
        Transaction.is_valid_transaction(transaction)



def test_valid_transaction_with_invalid_signature():
    sender_wallet = Wallet()
    recipient_address = "aaaabbbb"
    amount = 50
    transaction = Transaction(sender_wallet, recipient_address, amount) 
    transaction.input['signature'] = Wallet().sign(transaction.output)
    with pytest.raises(Exception, match="Signature is invalid"):
        Transaction.is_valid_transaction(transaction)
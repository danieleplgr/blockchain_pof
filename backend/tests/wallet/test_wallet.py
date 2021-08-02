from backend.wallet.wallet import Wallet


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

import requests, time
from backend.wallet.wallet import Wallet


BASE_URL = "http://localhost:5000"

def get_blockchain():
    return requests.get(f"{BASE_URL}/blockchain").json()

def get_blockchain_mine():
    return requests.get(f"{BASE_URL}/blockchain/mine").json()

def post_wallet_transact(recipient, amount): 
    return requests.post(
        f"{BASE_URL}/wallet/transact", 
        json= {"recipient_address": recipient, "amount": amount}
    ).json()

def get_wallet_info():
    return requests.get(f"{BASE_URL}/wallet/info").json()


wallet = Wallet()
start_blockchain = get_blockchain()
print(f"start_blockchain -> {start_blockchain}")

result_transact = post_wallet_transact(wallet.address, 20)
print(f"\n post_wallet_transact 1 -> {result_transact}")

time.sleep(1)

result_transact_2 = post_wallet_transact(wallet.address, 30)
print(f"\n post_wallet_transact 2 -> {result_transact_2}")

time.sleep(1)

mine_result = get_blockchain_mine()
print(f"\n mine_result -> {mine_result}")

wallet_info = get_wallet_info()
print(f"\n wallet_info -> {wallet_info}")
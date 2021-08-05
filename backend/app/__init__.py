import os, random, requests
from flask import Flask, jsonify, request
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSubManager
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool


app = Flask(__name__)
blockchain = Blockchain()
transactionPool = TransactionPool()
wallet = Wallet(blockchain)
pubSubManager = PubSubManager(blockchain, transactionPool)


@app.route("/")
def route_default():
    return "Blockchain rest api"


@app.route("/wallet/info")
def route_wallet_info():
    return jsonify({"address": wallet.address, "balance": wallet.balance})


@app.route("/blockchain")
def route_blockchain():
    return jsonify(blockchain.to_json())


@app.route("/blockchain/mine")
def route_blockchain_mine(): 
    transactions_as_json = transactionPool.get_transactions_as_json()
    reward_transaction = Transaction.create_reward_transaction(wallet).to_json()
    transactions_as_json.append(reward_transaction)
    blockchain.add_block(transactions_as_json)
    block = blockchain.chain[-1]
    pubSubManager.broadcast_block(block)
    transactionPool.clear_blockchain_transactions(blockchain)
    return jsonify(block.to_json())


@app.route("/wallet/transact", methods=["POST"])
def route_wallet_transact():
    transaction_data = request.get_json()
    transaction = transactionPool.existing_transaction(wallet.address)

    if transaction is not None:
        transaction.update(
            wallet,
            transaction_data['recipient_address'],
            transaction_data['amount'],
        )
    else:
        transaction = Transaction(
            wallet,
            transaction_data['recipient_address'],
            transaction_data['amount'],
        )
    
    pubSubManager.broadcast_transaction(transaction)
    return jsonify(transaction.to_json())



ROOT_PORT = 5000
PORT = ROOT_PORT
if os.environ.get("PEER") == "True":
    PORT = random.randint(5001,6000)
    result = requests.get(f"http://localhost:{ROOT_PORT}/blockchain") 
    try:
        remote_blockchain = Blockchain.from_json(result.json())
        blockchain.replace_chain(remote_blockchain.chain)
        print(f"Local chain synch with success")
    except Exception as e:
        print(f"Error on sync local chain => {e}")


app.run(port=PORT)
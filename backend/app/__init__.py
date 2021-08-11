import os, random, requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSubManager
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool


app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': "http://localhost:3000"} })
blockchain = Blockchain()
transactionPool = TransactionPool()
wallet = Wallet(blockchain)
pubSubManager = PubSubManager(blockchain, transactionPool, wallet)


@app.route("/")
def route_default():
    return "Blockchain rest api"


@app.route("/wallet/know-addresses")
def route_wallet_know_addresses():
    know_addresses = set()
    for block in blockchain.chain:
        for transaction in block.data: 
            know_addresses.update(transaction['output'].keys()) 
    return jsonify(list(know_addresses))


@app.route("/transactions")
def route_transactions(): 
    return jsonify(transactionPool.get_transactions_as_json())


@app.route("/wallet/info")
def route_wallet_info():
    return jsonify({"address": wallet.address, "balance": wallet.balance})


@app.route("/blockchain")
def route_blockchain():
    return jsonify(blockchain.to_json())


@app.route("/blockchain/range")
def route_blockchain_range():
    start = int(request.args.get("start"))
    end = int(request.args.get("end"))
    # [::-1] reverse order list
    return jsonify(blockchain.to_json()[::-1][start:end] )


@app.route("/blockchain/lenght")
def route_blockchain_lenght():
    return jsonify(len(blockchain.to_json()))


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



if os.environ.get("SEED_DATA") == "True":
    for i in range(10):
        blockchain.add_block([
            Transaction(Wallet(), Wallet().address, random.randint(2,50)).to_json(),
            Transaction(Wallet(), Wallet().address, random.randint(2,50)).to_json()
        ])
    for i in range(3):
        transactionPool.set_transaction(
            Transaction(Wallet(), Wallet().address, random.randint(2,50))
        )


app.run(port=PORT)
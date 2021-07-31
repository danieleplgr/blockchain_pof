import os, random, requests
from flask import Flask, jsonify
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSubManager


app = Flask(__name__)
blockchain = Blockchain()
pubSubManager = PubSubManager(blockchain)


@app.route("/")
def route_default():
    return "Blockchain rest api"


@app.route("/blockchain")
def route_blockchain():
    return jsonify(blockchain.to_json())


@app.route("/blockchain/mine")
def route_blockchain_mine():
    transaction_data = "stubbed_data"
    blockchain.add_block(transaction_data)
    block = blockchain.chain[-1]
    pubSubManager.broadcast_block(block)
    return jsonify(block.to_json())


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
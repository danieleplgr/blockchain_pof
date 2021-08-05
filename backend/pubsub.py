import time
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from backend.blockchain.block import Block
from backend.blockchain.blockchain import Blockchain
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool


CHANNELS = {
    "TEST": "TEST",
    "BLOCK": "BLOCK",
    "TRANSACTION": "TRANSACTION"
} 


class AppListener(SubscribeCallback):
    def __init__(self, blockchain: Blockchain, transactionPool: TransactionPool):
        self.blockchain = blockchain
        self.transactionPool = transactionPool

    
    def message(self, pubnub, message_event):
        print(f"\n Incoming message: {message_event.channel} => {message_event.message}")
        if message_event.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_event.message) 
            
            # slicing new list from start to end
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)
            try:
                self.blockchain.replace_chain(potential_chain)
                self.transactionPool.clear_blockchain_transactions(self.blockchain)
                print (f"\n Blochain replaced on received block message")
            except Exception as e:
                print (f"\n Error on replacing chain => {e}")
        
        elif message_event.channel == CHANNELS['TRANSACTION']:
            transaction = Transaction.from_json(message_event.message)
            self.transactionPool.set_transaction(transaction)
            print (f"\n Transaction set on received transaction message")






class PubSubManager():
    """
    Handle the channel pub/subscribe for the application, give communication between nodes of the network
    """
    def __init__(self, blockchain: Blockchain, transactionPool: TransactionPool):
        pnConfig = PNConfiguration()
        pnConfig.subscribe_key="sub-c-a0e92d96-f178-11eb-a38f-7e76ce3f98e8" 
        pnConfig.publish_key="pub-c-34c92741-0596-4980-be56-e5c0f34aef48"
        self.pubnub = PubNub(pnConfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(AppListener(blockchain, transactionPool))


    def publish(self, channel: str, event_message: object):
        #time.sleep(2)
        self.pubnub.publish().channel(channel).message(event_message).sync()


    def broadcast_block(self, block: Block):
        """
        Broadcast a new block to all the nodes of the network
        """
        self.publish(CHANNELS['BLOCK'], block.to_json())
    

    def broadcast_transaction(self, transaction: Transaction):
        """
        Broadcast a new transaction to all the nodes of the network
        """
        self.publish(CHANNELS['TRANSACTION'], transaction.to_json())



def main():    
    PubSubManager().publish(CHANNELS['TEST'], {"foo": "bar"})


if __name__ == '__main__':
    main()


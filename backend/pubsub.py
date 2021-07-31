import time
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from backend.blockchain.block import Block
from backend.blockchain.blockchain import Blockchain

CHANNELS = {
    "TEST": "TEST",
    "BLOCK": "BLOCK"
} 


class AppListener(SubscribeCallback):
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain

    
    def message(self, pubnub, message_event):
        print(f"\n Incoming message: {message_event.channel} => {message_event.message}")
        if message_event.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_event.message) 
            
            # slicing new list from start to end
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)
            try:
                self.blockchain.replace_chain(potential_chain)
                print (f"\n Blochain replaced on received block message")
            except Exception as e:
                print (f"\n Error on replacing chain => {e}")







class PubSubManager():
    """
    Handle the channel pub/subscribe for the application, give communication between nodes of the network
    """
    def __init__(self, blockchain: Blockchain):
        pnConfig = PNConfiguration()
        pnConfig.subscribe_key="sub-c-a0e92d96-f178-11eb-a38f-7e76ce3f98e8" 
        pnConfig.publish_key="pub-c-34c92741-0596-4980-be56-e5c0f34aef48"
        self.pubnub = PubNub(pnConfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(AppListener(blockchain))


    def publish(self, channel: str, event_message: object):
        #time.sleep(2)
        self.pubnub.publish().channel(channel).message(event_message).sync()


    def broadcast_block(self, block: Block):
        """
        Broadcast a new block to all the nodes of the network
        """
        self.publish(CHANNELS['BLOCK'], block.to_json())



def main():    
    PubSubManager().publish(CHANNELS['TEST'], {"foo": "bar"})


if __name__ == '__main__':
    main()


import uuid 
import json 
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    encode_dss_signature,
    decode_dss_signature
)
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
from backend.config import STARTING_BALANCE 


class Wallet():
    """
    An individual wallet for a miner.
    Permit to have transactions and store a balance.
    """
    def __init__(self, blockchain = None):
        self.address = str(uuid.uuid4())[0:8]
        self.private_key = ec.generate_private_key(
            ec.SECP256K1(), 
            default_backend()
        )
        self.public_key = Wallet.serialize_ec_public_key(self.private_key.public_key()) 
        self.blockchain = blockchain


    @property
    def balance(self):
        return Wallet.calculate_balance(self.blockchain, self.address)

    
    def sign(self, data: object):
        """
        Sign the data usign the private key
        """ 
        data_bytes = json.dumps(data).encode("utf-8")
        return decode_dss_signature(
            self.private_key.sign(data_bytes, ec.ECDSA(hashes.SHA256())) 
        ) 
    

    @staticmethod
    def serialize_ec_public_key(ec_public_key: "EllipticCurvePublicKey"):
        """
        Serialize public key 
        """
        return ec_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode("utf-8")


    @staticmethod
    def verify_signature(public_key: str, original_data, signed_data):
        """
        Verify the signature using the public data and original data
        """
        deserilized_pubk = serialization.load_pem_public_key(
            public_key.encode("utf-8"),
            default_backend()
        )

        (r, s) = signed_data 

        try:
            data_bytes = json.dumps(original_data).encode("utf-8")
            encoded_signed_data = encode_dss_signature(r, s)
            deserilized_pubk.verify(encoded_signed_data, data_bytes, ec.ECDSA(hashes.SHA256()))
            return True 
        except InvalidSignature as e:
            print("Invalid signature error")
            return False


    @staticmethod
    def calculate_balance(blockchain, address):
        """
        Calculate the balance of the given address considering the transactions in the blockchain data.
        The balance is found by adding the output vaòlue that belong to the address since the most recent transaction 
        in the blockchain
        """
        balance = STARTING_BALANCE

        if blockchain == None:
            return balance

        for block in blockchain.chain:
            for transaction in block.data: 
                # CASE address is a sender -> we reset to its change 
                # any time an address conduct a transaction reset its balance 
                if "input" in transaction and transaction['input']['address'] == address: 
                    balance = transaction['output'][address]
                # CASE address is a recipient in the transaction
                elif address in transaction['output']:
                    balance += transaction['output'][address]
        
        return balance



def main():
    wallet = Wallet()
    print(f"wallet => {wallet.__dict__}")
    original_data = {"foo": "bar"}
    data_signed = wallet.sign(original_data)
    print(f"data_signed => {data_signed}")
    valid_signature = wallet.verify_signature(wallet.public_key, original_data, data_signed)


if __name__=="__main__":
    main()
import uuid 
import json 
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
from backend.config import STARTING_BALANCE


class Wallet():
    """
    An individual wallet for a miner.
    Permit to have transactions and store a balance.
    """
    def __init__(self):
        self.address = str(uuid.uuid4())[0:8]
        self.private_key = ec.generate_private_key(
            ec.SECP256K1(), 
            default_backend()
        )
        self.public_key = self.private_key.public_key()
        self.balance = STARTING_BALANCE

    
    def sign(self, data: object):
        """
        Sign the data usign the private key
        """ 
        data_bytes = json.dumps(data).encode("utf-8")
        return self.private_key.sign(data_bytes, ec.ECDSA(hashes.SHA256()))
    

    @staticmethod
    def verify_signature(public_key, original_data, signed_data):
        """
        Verify the signature using the public data and original data
        """
        try:
            data_bytes = json.dumps(original_data).encode("utf-8")
            public_key.verify(signed_data, data_bytes, ec.ECDSA(hashes.SHA256()))
            return True 
        except InvalidSignature as e:
            print("Invalid signature error")
            return False




def main():
    wallet = Wallet()
    print(f"wallet => {wallet.__dict__}")
    original_data = {"foo": "bar"}
    data_signed = wallet.sign(original_data)
    print(f"data_signed => {data_signed}")
    valid_signature = wallet.verify_signature(wallet.public_key, original_data, data_signed)

if __name__=="__main__":
    main()
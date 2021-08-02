import uuid
import time 
from backend.wallet.wallet import Wallet


class Transaction():
    """
    Document of an exchange of currency from a sender to 1 or more recipients
    """
    def __init__(self, sender_wallet, recipient_address: str, amount: float):
        self.id = str(uuid.uuid4())[0:8]
        self.output = self.create_output(sender_wallet, recipient_address, amount)
        self.input = self.create_input(sender_wallet, self.output)
    


    def update(self, sender_wallet, recipient_address, amount):
        """
        Update the transaction with a new recipient 
        """
        if amount > self.output[sender_wallet.address]:
            raise Exception("amount exceed the balance")
        
        if recipient_address in self.output:
            self.output[recipient_address] = self.output[recipient_address] + amount
        else:
            self.output[recipient_address] = amount
        
        self.output[sender_wallet.address] = self.output[sender_wallet.address]- amount
        self.input = self.create_input(sender_wallet, self.output)



    def create_output(self, sender_wallet, recipient_address, amount):
        """
        Structure the output data for the transaction, each key contains an address and each value an amount
        """
        if amount > sender_wallet.balance:
            raise Exception("amount exceed the balance")

        output = {}
        # each transaction will have the recipient amount and the "change" that is the left amount in the sender 
        output[recipient_address] = amount 
        output[sender_wallet.address] = sender_wallet.balance - amount
        return output
    


    def create_input(self, sender_wallet, output):
        """
        Structure the input data for the transaction.
        Sign the transaction and include sender's public_key and address
        """
        input = {
            "timestamp": time.time_ns(),
            "amount": sender_wallet.balance,
            "address": sender_wallet.address,
            "public_key": sender_wallet.public_key,
            "signature": sender_wallet.sign(output)
        }
        return input


    @staticmethod
    def is_valid_transaction(transaction: object):
        """
        Validate a transaction, raise an exception in case of invalid one
        """
        output_total = sum(transaction.output.values())
        if transaction.input['amount'] != output_total:
            raise Exception("Invalid transaction output values")

        if not Wallet.verify_signature(
            transaction.input['public_key'],
            transaction.output,
            transaction.input['signature']
        ):
            raise Exception("Signature is invalid")


def main():
    sender_wallet = Wallet()
    recipient_address = "aaaabbbb"
    amount = 110
    transaction = Transaction(sender_wallet, recipient_address, amount)
    print(f"transaction >> {transaction.__dict__}")

if __name__=="__main__":
    main()
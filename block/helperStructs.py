from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization
import base64
from .helperfunctions import *
from .models import Wallet


class TransactionStruct:
    def __init__(self, sender_id, trxn_uuid, sender_pub_key, receiver_pub_key, amount, trxn_hash, trnx_signature):
        self.sender_id = sender_id
        self.trxn_uuid = trxn_uuid
        self.sender_pub_key = sender_pub_key
        self.receiver_pub_key = receiver_pub_key
        self.amount = amount
        self.trxn_hash = trxn_hash
        self.trnx_signature = trnx_signature

    def verify_transaction(self) -> bool:
        transaction_is_valid: bool = True
        if self.amount < 0:
            transaction_is_valid = False
            print("Invalid Transaction Amount!")
        try:
            # print(f'{base64.b64decode(self.trnx_signature.encode("utf-8"))}')
            # print(f'{self.trxn_hash}')
            serialization.load_pem_public_key(self.sender_pub_key.encode("utf-8")) \
                .verify(b64_to_binary(self.trnx_signature), bytes(self.trxn_hash, "utf-8"))
                # .verify(base64.b64decode(self.trnx_signature.encode("utf-8")), bytes(self.trxn_hash, "utf-8"))
            print("Signature is valid")
        except:
            print("Transaction signature is invalid!")
            # print(self.trnx_signature.encode('unicode_escape').decode('latin1').encode('latin1'))
            # print(self.trnx_signature.encode("latin1"))
            transaction_is_valid = False

        # check if user has the funds to make this transaction
        try:
            user_wallet_balance = Wallet.objects.get(pk=self.sender_id).balance
        # print(user_wallet_balance)
            if self.amount > user_wallet_balance:
                print("The user doesn't have the funds to make this transaction")
                transaction_is_valid = False
        except:
            print("This user doesn't exist")
            transaction_is_valid = False


        return transaction_is_valid

    def print(self):
        print(f"""
        Sender Id: {self.sender_id}
        Transaction UUID: {self.trxn_uuid},
        Sender Public Key: {self.sender_pub_key},
        Receiver Public Key: {self.receiver_pub_key},
        Transaction Amount: {self.amount},
        Transaction Hash: {self.trxn_hash},
        Transaction Signature: {self.trnx_signature}
""")




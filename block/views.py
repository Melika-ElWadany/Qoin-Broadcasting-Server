from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Block, Transaction, Wallet
from . import serializers
from rest_framework import status
from .helperStructs import TransactionStruct
import hashlib
from .serializers import TransactionSerializer


@api_view(["GET"])
def get_blocks(request):
    blocks = Block.objects.all()
    serialized_blocks = serializers.BlockSerializer(blocks, many=True)
    return Response(serialized_blocks.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_block_transaction(request, block_id):
    transactions = Transaction.objects.filter(parent_block=block_id)
    serialized_transactions = serializers.TransactionSerializer(transactions, many=True)
    return Response(serialized_transactions.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def new_transaction(request):
    # ntd = New Transaction Data
    ntd = request.data
    # print(ntd)
    new_transaction_obj = Transaction(sender_id=ntd.get("sender_id"), trxn_uuid=ntd.get("trxn_uuid"),
                                      sender_pub_key=ntd.get("sender_pub_key"), amount=ntd.get("amount"),
                                      receiver_pub_key=ntd.get("receiver_pub_key"), trxn_hash=ntd.get("trxn_hash"),
                                      trxn_signature=ntd.get("trxn_signature"))
    new_transaction_obj.save()
    print("lala")
    return Response({"test-new_transaction-route": "test-new_transaction-route"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_wallet_balance(request, sender_id):
    wallet = Wallet.objects.get(pk=sender_id)
    resp = {"wallet_balance": wallet.balance}
    return Response(resp, status=status.HTTP_200_OK)


@api_view(["POST", "GET"])
def new_block(request):
    # Get the new block data
    new_block_data = request.data
    all_transaction_are_valid = True
    new_block_hash = ""
    # For each transaction, create a TransactionStruct object
    transactions = [TransactionStruct(tr.get("sender_id"), tr.get("trxn_uuid"), tr.get("sender_pub_key"), tr.get("receiver_pub_key"),
                                      tr.get("amount"), tr.get("trxn_hash"), tr.get("trxn_signature"))
                    for tr in new_block_data.get("transactions")]
    # Check if all the transactions in the block are valid
    for tr in transactions:
        tr.print()
        if not(tr.verify_transaction()):
            all_transaction_are_valid = False

    # if the transactions are valid, hash their uuids, get the previous block hash,
    # append it to the uuid string, and hash it produce the block's hash
    if all_transaction_are_valid:
        all_transactions_hashes_as_str = "".join([trxn.trxn_hash for trxn in transactions])
        previous_block_hash = Block.objects.all().last().hash
        new_block_hash_ingest = all_transactions_hashes_as_str + previous_block_hash
        # print(all_transactions_hashes_as_str)
        # print(previous_block_hash.hash)
        new_block_hash = hashlib.sha256((bytes(new_block_hash_ingest, 'utf-8'))).hexdigest()
        print(new_block_hash)

    return Response({"test": "test"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_pending_transactions(request):
    pending_transactions = Transaction.objects.filter(status="pending")[:10]
    serialized_pending_transactions = TransactionSerializer(pending_transactions, many=True)
    return Response(serialized_pending_transactions.data, status=status.HTTP_200_OK)


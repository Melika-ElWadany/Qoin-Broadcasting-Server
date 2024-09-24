from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Block, Transaction
from . import serializers
from rest_framework import status
from .helperStructs import TransactionStruct
import hashlib


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

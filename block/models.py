from django.db import models


class Block(models.Model):
    hash = models.CharField(max_length=200)
    prev_block_hash = models.CharField(max_length=200)


class Transaction(models.Model):
    trnx_uuid = models.CharField(max_length=200)
    sender_pub_key = models.CharField(max_length=200)
    receiver_pub_key = models.CharField(max_length=200)
    amount = models.IntegerField()
    trnx_hash = models.CharField(max_length=200)
    trnx_signature = models.BinaryField()
    parent_block = models.ForeignKey(Block, on_delete=models.CASCADE)


class Wallet(models.Model):
    private_key = models.CharField(max_length=200)
    public_key = models.CharField(max_length=200)
    balance = models.IntegerField()


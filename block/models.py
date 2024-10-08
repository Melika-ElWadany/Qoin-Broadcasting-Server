from django.db import models
choices = [("pending", "pending"), ("verified", "verified")]


class Block(models.Model):
    hash = models.CharField(max_length=200)
    prev_block_hash = models.CharField(max_length=200)


class Transaction(models.Model):
    sender_id = models.IntegerField()
    trxn_uuid = models.CharField(max_length=200)
    sender_pub_key = models.CharField(max_length=200)
    receiver_pub_key = models.CharField(max_length=200)
    amount = models.IntegerField()
    trxn_hash = models.CharField(max_length=200)
    trxn_signature = models.CharField(max_length=200)
    parent_block = models.ForeignKey(Block, on_delete=models.CASCADE, default=1)
    status = models.CharField(choices=choices, max_length=20, default="pending")


class Wallet(models.Model):
    private_key = models.CharField(max_length=200)
    public_key = models.CharField(max_length=200)
    balance = models.IntegerField()


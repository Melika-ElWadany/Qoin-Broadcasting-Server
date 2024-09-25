from django.urls import path
from . import views

urlpatterns = [
    path("all/", views.get_blocks, name="all-blocks"),
    path("<block_id>/transactions/", views.get_block_transactions, name="block-transactions"),
    path("new/", views.new_block, name="new-block"),
    path("transactions/new/", views.new_transaction, name="new-transaction"),
    path("transactions/pending/", views.get_pending_transactions, name="get-pending-transactions"),
    path("wallets/balance/<sender_id>/", views.get_wallet_balance, name="get-wallet-balance"),
]
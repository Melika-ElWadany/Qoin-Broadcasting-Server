from django.urls import path
from . import views

urlpatterns = [
    path("all/", views.get_blocks, name="all-blocks"),
    path("<block_id>/transactions/", views.get_block_transaction, name="block-transactions"),
    path("new/", views.new_block, name="new-block")
]
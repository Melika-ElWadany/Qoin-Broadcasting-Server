# Generated by Django 5.1.1 on 2024-09-24 15:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0005_transaction_sender_id_transaction_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='parent_block',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='block.block'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='trnx_signature',
            field=models.CharField(max_length=200),
        ),
    ]

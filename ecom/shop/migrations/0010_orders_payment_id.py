# Generated by Django 4.2.4 on 2023-09-29 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_orderupdate_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='payment_id',
            field=models.CharField(default='', max_length=90),
        ),
    ]

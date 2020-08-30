# Generated by Django 3.0.8 on 2020-08-22 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], default='pending', max_length=200, null=True),
        ),
    ]
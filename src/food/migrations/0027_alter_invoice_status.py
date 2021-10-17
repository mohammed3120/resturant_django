# Generated by Django 3.2.7 on 2021-10-09 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0026_invoice_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('ToAccepted', 'ToAccept'), ('InProgress', 'InProgress'), ('Delivered', 'Delivered'), ('Canceled', 'Canceled')], default='Pending', max_length=50),
        ),
    ]

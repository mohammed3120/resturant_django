# Generated by Django 3.2.7 on 2021-09-26 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0016_remove_order_delivary_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
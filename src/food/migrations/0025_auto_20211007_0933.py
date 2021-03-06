# Generated by Django 3.2.7 on 2021-10-07 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0024_auto_20211007_0931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='ceated',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='meal',
            name='ceated',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='meal',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

# Generated by Django 3.2.7 on 2021-09-17 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0005_auto_20210917_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='specific_address',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]

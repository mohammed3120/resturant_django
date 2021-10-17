# Generated by Django 3.2.7 on 2021-09-29 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0017_alter_order_order_date'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ingrediant',
            new_name='Ingredient',
        ),
        migrations.RemoveField(
            model_name='meal',
            name='ingrediants',
        ),
        migrations.AddField(
            model_name='meal',
            name='ingredients',
            field=models.ManyToManyField(to='food.Ingredient'),
        ),
    ]
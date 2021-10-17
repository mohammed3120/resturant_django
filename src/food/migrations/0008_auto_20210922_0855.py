# Generated by Django 3.2.7 on 2021-09-22 05:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0007_item_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='is_head',
            new_name='is_admin',
        ),
        migrations.RemoveField(
            model_name='meal',
            name='category',
        ),
        migrations.AddField(
            model_name='meal',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='food.department'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]

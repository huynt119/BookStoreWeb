# Generated by Django 5.0.4 on 2024-05-07 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='item_id',
            new_name='item',
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='user_id',
            new_name='user',
        ),
    ]

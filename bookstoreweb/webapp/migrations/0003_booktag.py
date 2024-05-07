# Generated by Django 5.0.4 on 2024-05-07 16:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_rename_item_id_rating_item_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.tag')),
                ('item_tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.book')),
            ],
        ),
    ]

# Generated by Django 3.1.1 on 2020-10-05 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20201005_0901'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='category_id',
            new_name='category',
        ),
    ]
# Generated by Django 3.2.8 on 2021-12-01 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20211130_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesskeysandtokens',
            name='twitter_access_token',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='accesskeysandtokens',
            name='twitter_access_token_secret',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='accesskeysandtokens',
            name='twitter_api_key',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='accesskeysandtokens',
            name='twitter_api_key_secret',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='accesskeysandtokens',
            name='twitter_bearer_token',
            field=models.BinaryField(),
        ),
    ]
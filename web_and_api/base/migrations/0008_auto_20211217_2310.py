# Generated by Django 3.2.8 on 2021-12-17 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_auto_20211217_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesskeysandtokens',
            name='twitter_access_token',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='accesskeysandtokens',
            name='twitter_access_token_secret',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='accesskeysandtokens',
            name='twitter_api_key',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='accesskeysandtokens',
            name='twitter_bearer_token',
            field=models.CharField(max_length=255),
        ),
    ]

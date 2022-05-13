from django.db import models
from base.models import AccessKeysAndTokens, User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['date_updated', 'visibility', 'org', 'password']


class AccessKeysAndTokensSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessKeysAndTokens
        exclude = ['visibility', 'date_updated']

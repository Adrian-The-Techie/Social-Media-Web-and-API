from rest_framework import serializers
from . models import Organisation, AccessKeysAndTokens


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        exclude = ['visibility', 'date_updated']

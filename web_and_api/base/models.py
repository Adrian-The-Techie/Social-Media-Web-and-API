from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    id_number = models.IntegerField(default=0, null=True)
    phone = models.CharField(
        max_length=255, null=False, default="+254700000000")
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(blank=True, null=True)
    visibility = models.IntegerField(default=True)
    url = models.UUIDField(max_length=255, null=True)
    org = models.IntegerField(default=1, null=True)
    role = models.IntegerField(default=1, null=True)

    def __str__(self):
        return self.first_name


class Organisation(models.Model):
    name = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(blank=True, null=True)
    visibility = models.IntegerField(default=True)
    url = models.UUIDField(max_length=255, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class AccessKeysAndTokens(models.Model):

    org = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    page_name = models.CharField(max_length=255)
    twitter_api_key = models.CharField(max_length=255)
    twitter_api_key_secret = models.CharField(max_length=255)
    twitter_access_token = models.CharField(max_length=255)
    twitter_access_token_secret = models.CharField(max_length=255)
    twitter_bearer_token = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(blank=True, null=True)
    visibility = models.IntegerField(default=True)
    created_by = models.IntegerField(default=1, null=True)
    updated_by = models.IntegerField(default=1, null=True)
    url = models.UUIDField(null=True)

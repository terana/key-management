import uuid
from datetime import datetime

from django.contrib.auth.models import (
    AbstractUser
)
from django.db import models
from django_cryptography.fields import encrypt


class Client(AbstractUser):
    display_name = models.CharField(max_length=128)


class Secret(models.Model):
    key = models.CharField(max_length=32, primary_key=True)
    value = encrypt(models.CharField(max_length=32))


class ACLRule(models.Model):
    uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4, editable=False)
    acl = models.CharField(max_length=32, unique=True)
    secret = models.CharField(max_length=32)
    read = models.BooleanField(default=False)
    update = models.BooleanField(default=False)
    create = models.BooleanField(default=False)


class AccessLog(models.Model):
    uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4, editable=False)
    time = models.DateTimeField(default=datetime.utcnow)
    requested_secret = models.CharField(max_length=32)
    result = models.BooleanField(default=False)
    exception = models.BooleanField(default=False)


class TokenACL(models.Model):
    uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4, editable=False)
    token_id = models.ForeignKey(Client, related_name='token',
                                 on_delete=models.CASCADE)
    acl = models.ForeignKey(ACLRule, to_field='acl', db_column='acl',
                            on_delete=models.CASCADE)

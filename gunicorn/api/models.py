from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import datetime
import uuid


class Secret(models.Model):
	key = models.CharField(max_length=32, unique=True, primary_key=True)
	value = models.CharField(max_length=32, unique=True)


class Token(models.Model):
	value = models.CharField(max_length=32, unique=True, primary_key=True,
							 editable=False)
	display_name = models.CharField(max_length=32, unique=True)
	source = models.CharField(max_length=32, unique=True, editable=False)


class TokenACL(models.Model):
	uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4, editable=False)
	token_id = models.ForeignKey(Tokens, related_name='token',
                                on_delete=models.CASCADE)
	acl = models.ForeignKey(ACLRules, to_field='acl', db_column='acl',
                                on_delete=models.CASCADE)


class ACLRule(models.Model):
	uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4, editable=False)
	acl = models.CharField(max_length=32)
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

from django.db import models
from .helpers import model_helpers as helper

import datetime as dt
import uuid

class Uuid(models.Model):
    id = models.UUIDField(primary_key = True, editable = False, default = uuid.uuid4)

    class Meta:
        abstract = True

class Users(Uuid):
    name = models.CharField(max_length = 100, unique = True)
    image_url = models.CharField(max_length = 256)
    personal_color = models.CharField(max_length = 7)

class Groups(Uuid):
    owner_id = models.ForeignKey("Users", on_delete = models.CASCADE)
    name = models.CharField(max_length = 100, unique = True)
    category = models.CharField(max_length = 50)
    icon = models.CharField(max_length = 20)
    banner_color = models.CharField(max_length = 7)
    icon_background_color = models.CharField(max_length = 7)

class GroupsMembers(Uuid):
    user_id = models.ForeignKey("Users", on_delete = models.CASCADE)
    group_id = models.ForeignKey("Groups", on_delete = models.CASCADE)
    is_owner = models.BooleanField()

class Messages(Uuid):
    user_id = models.ForeignKey("Users", on_delete = models.CASCADE, related_name = "user_id")
    group_id = models.ForeignKey("Groups", on_delete = models.CASCADE)
    reply_to_id = models.ForeignKey("Users", on_delete = models.SET_NULL, related_name = "reply_to_id", default = None, blank = True, null = True)
    message = models.CharField(max_length = 1000)
    date = models.DateTimeField(default = dt.datetime.now)
    location = models.CharField(max_length = 50)
    image_url = models.CharField(max_length = 256)

class Notifications(Uuid):
    user_id = models.ForeignKey("Users", on_delete = models.CASCADE)
    message = models.CharField(max_length = 200)
    date = models.DateTimeField(default = dt.datetime.now)

class SignInData(models.Model):
    email = models.CharField(primary_key = True, unique = True, max_length = 30)
    user_id = models.ForeignKey("Users", models.CASCADE)
    password = models.CharField(max_length = 100)

class SessionTokens(models.Model):
    token = models.CharField(primary_key = True, editable = False, unique = True, max_length = 50)
    user_id = models.ForeignKey("Users", models.CASCADE)
    date = models.DateTimeField(default = helper.token_date)
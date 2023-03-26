from django.db import models
from .helpers.model_helpers import token_date, generate_name

import datetime as dt
import uuid

class Uuid(models.Model):
    id = models.UUIDField(primary_key = True, editable = False, default = uuid.uuid4)

    class Meta:
        abstract = True

class User(Uuid):
    name = models.CharField(max_length = 100, unique = True, default = generate_name)
    image_url = models.CharField(max_length = 256, default = "")
    personal_color = models.CharField(max_length = 7, default = "#ffffff")

class Group(Uuid):
    owner_id = models.ForeignKey("User", on_delete = models.CASCADE)
    name = models.CharField(max_length = 100, unique = True)
    category = models.CharField(max_length = 50)
    icon = models.CharField(max_length = 20)
    banner_color = models.CharField(max_length = 7)
    icon_background_color = models.CharField(max_length = 7)

class GroupsMember(Uuid):
    user_id = models.ForeignKey("User", on_delete = models.CASCADE)
    group_id = models.ForeignKey("Group", on_delete = models.CASCADE)
    is_owner = models.BooleanField()

class Message(Uuid):
    user_id = models.ForeignKey("User", on_delete = models.CASCADE, related_name = "user_id")
    group_id = models.ForeignKey("Group", on_delete = models.CASCADE)
    reply_to_id = models.ForeignKey("User", on_delete = models.SET_NULL, related_name = "reply_to_id", default = None, blank = True, null = True)
    message = models.CharField(max_length = 1000)
    date = models.DateTimeField(default = dt.datetime.now)
    location = models.CharField(max_length = 50)
    image_url = models.CharField(max_length = 256)

class Notification(Uuid):
    user_id = models.ForeignKey("User", on_delete = models.CASCADE)
    message = models.CharField(max_length = 200)
    date = models.DateTimeField(default = dt.datetime.now)

class SignInData(models.Model):
    email = models.EmailField(primary_key = True, unique = True, max_length = 30)
    user_id = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)

class SessionToken(models.Model):
    token = models.CharField(primary_key = True, unique = True, max_length = 100)
    user_id = models.CharField(max_length = 100)
    date = models.DateTimeField(default = token_date)
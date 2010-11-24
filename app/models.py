from django.db import models
from google.appengine.ext import db

class User(models.Model):
    user_id = models.CharField(max_length=35)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    fb_id = models.CharField(max_length=32)
    auth_token = models.CharField(max_length=50)
    auth_token_key = models.CharField(max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)

class ThayResponse(models.Model):
    user = models.ForeignKey(User)
    response_id = models.CharField(max_length=32)
    question_id = models.CharField(max_length=32)

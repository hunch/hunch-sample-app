from appengine_django.models import BaseModel
from google.appengine.ext import db

class User(BaseModel):
    user_id = db.StringProperty()
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    fb_id = db.StringProperty()
    auth_token = db.StringProperty()
    auth_token_key = db.StringProperty()
    date_joined = db.DateTimeProperty('date joined')

class ThayResponse(BaseModel):
    user = db.ReferenceProperty(User)
    response_id = db.StringProperty()
    question_id = db.StringProperty()

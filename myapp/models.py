from django.db import models
from django.contrib.auth import get_user_model

# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Column,Integer,String

# db = SQLAlchemy()


# Create your models here.
# class User(db.Model):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     password = Column(String)

User = get_user_model()

class WebhookEvent(models.Model):
    event_type = models.CharField(max_length=100)
    reference_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50)
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reference_id
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username
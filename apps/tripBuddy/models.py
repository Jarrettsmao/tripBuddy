from __future__ import unicode_literals
from django.db import models
import re
from datetime import date

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'[A-Za-z]')
class TripManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        if len(postData['fname']) < 2 or not NAME_REGEX.match(postData['fname']):
            errors['fname'] = "First name must contain at least 2 letters!"
        if len(postData['lname']) < 2 or not NAME_REGEX.match(postData['fname']):
            errors['lname'] = "Last name must contain at least 2 letters!"
        if postData['rPass'] != postData['crPass']:
            errors['matchPass'] = "Passwords do not match!"
        if not EMAIL_REGEX.match(postData['email']):
            errors['invEmail'] = "Invalid email!"
        if User.objects.filter(email=postData['email']).count() == 1:
            errors['usedEmail'] = "Email already taken!"
        if len(postData['rPass']) < 8:
            errors['lenPass'] = "Passwords must be at least 8 characters long!"
        return errors
    def trip_validator(self, postData):
        errors = {}
        if len(postData['dest']) < 3:
            errors['dest'] = "A trip destination must contain at least 3 characters!"
        if len(postData['plan']) < 3:
            errors['plan'] = "A plan must be provided!"
        today = date.today()
        if postData['sDate'] < str(today) or postData['eDate'] < postData['sDate']:
            errors['sDate'] = "Please choose a valid start date!"
        if postData['eDate'] < postData['sDate'] or postData['eDate'] < str(today):
            errors['eDate'] = "Please choose a valid end date!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

class Trip(models.Model):
    destination = models.CharField(max_length=45)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField()
    
    creator = models.ForeignKey(User, related_name="createdTrips")
    vacationer = models.ManyToManyField(User, related_name="joinedTrips", null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
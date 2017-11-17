from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime, timedelta

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile("^[a-zA-Z._-]+$")
PASSWORD_REGEX = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")

# GENDER_CHOICES = (
#    ('M', 'Male'),
#    ('F', 'Female')
# )


class UserManager(models.Manager):
    def basica_validator(self, postData):
        errors = {}

        if postData['first_name'] == '' or postData['last_name'] == '':
            errors['name'] = 'Name can not be blank.'
        else:
            if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
                errors['name'] = 'Name can not be less than 2 characters.'
            else:
                if not NAME_REGEX.match(postData['first_name']) or not NAME_REGEX.match(postData['last_name']):
                    errors['name'] = 'Please input valid name. Letters only.'

        if postData['email'] == '':
            errors['email'] = 'Email can not be blank.'
        else:
            if not EMAIL_REGEX.match(postData['email']):
                errors['email'] = 'Please input valid email.'
            else:
                if len(self.filter(email=postData['email']))>0:
                    errors['email'] = 'email already in use.'

        if postData['password'] == '':
            errors['password'] = 'Password can not be blank.'
        else:
            if len(postData['password']) < 2:
                errors['password'] = 'Password can not be less than 8 characters.'
            else:
                if not PASSWORD_REGEX.match(postData['password']):
                    errors['password'] = 'Please input valid email.'
                if postData['password'] != postData['cpassword']:
                    errors['password'] = 'Password does not match.'
        
        if postData['date'] !='':
            date = datetime.strptime(postData['date'], "%Y-%m-%d")
            now = datetime.now()
            if date > now:
                errors['date'] = 'Birthday date can not be after today.'
            else:
                if date - now < timedelta(567648000):
                    errors['date'] = 'Can not register due to under age.'

        else:
            errors['date'] = 'Birthday date is invalid.'

        return errors
        # return dictionary

    def login_validator(self, postData):
        errors = {}

        if postData['email'] == '':
                errors['email'] = 'Email can not be blank.'

        if postData['password'] == '':
            errors['password'] = 'Password can not be blank.'

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateTimeField(auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=128)
    objects = UserManager()

    # choices=GENDER_CHOICES, 

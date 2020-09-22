from django.db import models
import re


class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['first_name']) < 3:
            errors['first_name'] = "First name must be at least 3 characters"
        if len(postData['last_name']) < 3:
            errors['last_name'] = "Last name must be at least 2 characters"
        if len(postData['email']) < 8:
            errors['email_length'] = "Email is too short"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_regex'] = "Invalid email address"
        if len(postData['password']) < 8:
            errors['pw_length'] = "Passwords must be at least 8 characters"
        if postData['password'] != postData['confirmed_pw']:
            errors['invalid_pw'] = "Passwords do not match"
        return errors

    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_regex'] = "Invalid email address"
        if len(postData['password']) < 8:
            errors['password'] = "Passwords must be at least 8 characters"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

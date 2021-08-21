from django.db import models
import re
import bcrypt
from datetime import *
# Create your models here.

            
class UserManager(models.Manager):
    def register_validator(self, postData):

        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        existing_user = User.objects.filter(email = postData['email'])

        errors = {}
        
        if len(postData['first_name']) == 0:
            errors['first_name'] = "First Name is required"

        elif len(postData['first_name']) < 2:
            errors['first_name_len'] = "First Name should be at least 2 characters long"

        if len(postData['last_name']) == 0:
            errors['last_name'] = "Last Name is required."

        elif len(postData['last_name']) < 2:
            errors['last_name_len'] = "Last Name should be at least 2 characters long"
        
        if len(existing_user) > 0:
            errors['duplicate'] = "That email is already taken, please provide an other email"

        if len(postData['email']) == 0:
            errors['email'] = "Please enter your email"

        elif not EMAIL_REGEX.match(postData['email']):
            errors['email_pattern'] = "Invalid email address!"


        if len(postData['pwd']) == 0:
            errors['pwd'] = "Password is required"
        
        elif len(postData['pwd']) < 8:
            errors['pwd_len'] = "Password should be at least 8 characters long"

        if postData['pwd'] != postData['confirm_pwd']:
            errors['mismatch'] = "Passwords do not match"

        return errors

    def login_validator(self, postData):

        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        existing_user = User.objects.filter(email = postData['email'])

        errors = {}

        if len(postData['email']) == 0:
            errors['email'] = "Please enter your email"

        elif len(existing_user) == 0:
            errors['non_match'] = "That email is not registered"
            return errors
        
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email_pattern'] = ("Invalid email address!")        

        elif len(postData['pwd']) == 0:
            errors['pwd'] = "Password is required to login"

        elif bcrypt.checkpw(postData['pwd'].encode(), existing_user[0].pwd.encode()) != True:
            errors['no_match'] = "Please enter a valid email and password"

        return errors

class JobManager(models.Manager):
    def job_validator(self, postData):
        errors = {}
        if len(postData['ttl']) == 0:
            errors['title'] = 'Job title must be provided'
        elif len(postData['ttl']) < 3:
            errors['ttl'] = 'Job title should be at least 3 characters long'
        if len(postData['dsc']) == 0:
            errors['description'] = 'Job description must be provided'
        elif len(postData['dsc']) < 3:
            errors['dsc'] = 'Job description should be at least 3 characters long'
        if len(postData['lctn']) == 0:
            errors['lct'] = 'Job location must be provided'
        elif len(postData['lctn']) < 3:
            errors['lctn'] = 'Job location should be at least 3 characters long'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    pwd = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.email

class Job(models.Model):
    title = models.CharField(max_length=255)
    dsc = models.CharField(max_length=255)
    lctn = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name="jobs", on_delete=models.CASCADE)
    favorites = models.ManyToManyField(User, related_name="favorite_jobs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()
from django.db import models
import re
import bcrypt


# Create your models here.
class UserManager(models.Manager):
    def register_validator(self, post_data):
        errors = {}

        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters"

        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters"

        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Email/Password is incorrect. Please try again."

        if len(post_data['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"

        if (post_data['password'] != post_data['password_confirm']):
            errors['password_confirm'] = "Password confirm didn't match"

        user_list = User.objects.filter(email=post_data['email'])
        if (len(user_list) > 0):
            errors['email_password'] = 'Email/password is incorrect. Please try again.'

        return errors

    def login_validator(self, post_data):
        errors = {}
        users_list = User.objects.filter(email=post_data['email'])
        if len(users_list) == 0:
            errors['email_password'] = "Email/password is incorrect. Please try again."
        else:
            if bcrypt.checkpw(
                post_data['password'].encode(),
                users_list[0].password.encode()
            ) != True:
                errors['email_password'] = "Email/password is incorrect. Please try again."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    #username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class JobManager(models.Manager):
    def job_validator(self, post_data):
        errors = {}

        if len(post_data['title']) < 3:
            errors['title'] = "A job must consist of at least 3 characters!"

        if len(post_data['location']) <= 0:
            errors['location'] = "A location must be provided!"

        return errors

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()

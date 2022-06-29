from django.db import models
import re

# Create your models here.

class UserManager(models.Manager):

    def basic_validator(self, postData,user = None):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

#==========================================================================================
        if not postData["first_name"]:
            errors["first_name"] = "Please enter your first name "

        elif len(postData["first_name"]) < 3 :
            errors["first_name"] = "First name should be at least 3 characters"

        elif not postData["first_name"].isalpha():
            errors["first_name"] = "First name should be only letters"

        if not postData["last_name"]:
            errors["last_name"] = "Please enter your last name "

        elif len(postData["last_name"]) < 3 :
            errors["last_name"] = "last name should be at least 3 characters"

        elif not postData["last_name"].isalpha():
            errors["last_name"] = "last name should be only letters"
        if not postData["email"]:
            errors["email"] = "Please enter your email "

        elif not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = "Invalid email address!"

        else:
            if user is None or user.email != postData["email"]:
                
                if User.objects.filter(email=postData["email"]).exists():
                    errors["email"] = "This email is already exist, please try another one"

#==========================================================================================
        if not postData["password"]: 
            errors["password"] = "Please enter your password "
            
        elif len(postData['password']) < 8 :
            errors["password"] = "Password should be at least 8 characters"

        elif not re.match(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$', postData['password']):
            errors["password"] = "password should be strong"

        if not postData["confirmPW"]:
            errors["confirmPW"] ="Please enter your password confirmation "

        
        elif postData["confirmPW"] != postData["password"]:
                errors["confirmPW"] = "The passwords don't match"

        

        return errors

#=========================================================================================
    def login_basic_validator(self, postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not postData["email"]:
            errors["email"] = "Please enter your email "

        elif not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = "Invalid email address!"
#==========================================================================================
        if not postData["password"]: 
            errors["password"] = "Please enter your password "
            
        elif len(postData['password']) < 8 :
            errors["password"] = "Password should be at least 8 characters"

        return errors
#==========================================================================================
    def update_basic_validator(self, postData,user = None):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not postData["email"]:
            errors["email"] = "Please enter your email "

        elif not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = "Invalid email address!"

        else:
            if user is None or user.email != postData["email"]:
                if User.objects.filter(email=postData["email"]).exists():
                    errors["email"] = "This email is already exist, please try another one"

        if not postData["first_name"]:
            errors["first_name"] = "Please enter your first name "

        elif len(postData["first_name"]) < 3 :
            errors["first_name"] = "First name should be at least 3 characters"

        elif not postData["first_name"].isalpha():
            errors["first_name"] = "First name should be only letters"

        if not postData["last_name"]:
            errors["last_name"] = "Please enter your last name "

        elif len(postData["last_name"]) < 3 :
            errors["last_name"] = "last name should be at least 3 characters"

        elif not postData["last_name"].isalpha():
            errors["last_name"] = "last name should be only letters"

        return errors
#==========================================================================================
        

        
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    desc=models.TextField(blank=True)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField('is_admin',  default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()


class Message(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, related_name="messages", on_delete=models.CASCADE)
    for_user = models.ForeignKey(User,related_name="usermessages", on_delete=models.CASCADE,blank=True,null=True)
        


class Comment(models.Model):
    user = models.ForeignKey(
        User, related_name="comments", on_delete=models.CASCADE)
    message = models.ForeignKey(
        Message, related_name="comments", on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

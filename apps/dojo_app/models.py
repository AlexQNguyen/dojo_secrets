from __future__ import unicode_literals

from django.db import models

# Create your models here.
from datetime import datetime, timedelta

import bcrypt, re

# Create your models here.
class UserManager(models.Manager):
    def validate(self, postData):
        errors = [] # make a list of errors
        #first name validation
        if len(postData['first_name']) == 0:
            errors.append('Please Enter First Name.')
        elif len(postData['first_name']) < 2:
            errors.append('First Name must be between 3-45 characters')
        elif not re.search(r'^[A-Za-z]+$', postData['first_name']):
            errors.append('First name must only contain letters')
        #last_name validation
        if len(postData['last_name']) == 0:
            errors.append('Please Enter a Last Name.')
        elif len(postData['last_name']) < 2:
            errors.append('Last Name must be between 3-45 characters')
        elif not re.search(r'^[A-Za-z]+$', postData['last_name']):
            errors.append('Last Name must only contain letters')
        #email validation
        if len(postData['email']) == 0:
            errors.append('Email cannot be left blank')
        elif not re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$',postData['email']):
            errors.append('You have entered an invalid Email')
        elif len(User.objects.filter(email=postData['email']))>0:
            errors.append('This email is already registered')
        #password validation
        if len(postData['password']) < 7:
            errors.append('Password must be at least 8 characters')
        if postData['confirm'] != postData['password']:
            errors.append('Password and confirm password does not match')
        #Date of birth Validation
        try:
            dob = datetime.strptime(postData['dob'], '%m/%d/%Y')
            if datetime.now() < dob:
                errors.append('DOB cannot be in the future')
        except ValueError:
            errors.append('Invalid date entry, must be mm/dd/yyyy')

        # still need the validation of DOB format mm/dd/yyyy
        if len(errors)== 0:
            user = User.objects.create(first_name=postData['first_name'], last_name= postData['last_name'], email=postData['email'],dob=dob, pw_hash=bcrypt.hashpw(postData['password'].encode(),bcrypt.gensalt()))
            return (True, user)


        return(False, errors)
    #login Authentication
    def authenticate(self, postData):
        if 'email' in postData and 'password' in postData:
            try:
                user = User.objects.get(email=postData['email'])

            except User.DoesNotExist:
                return(False, 'Invalid email, or password does not match email')

            u = user.pw_hash.encode()
            pw_match = bcrypt.hashpw(postData['password'].encode(),u)
            if pw_match == u:
                return (True, user)
            else:
                return (False, 'Email and password combination do not match')
        else:
            return (false, 'Please enter Login information')



class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    dob = models.DateTimeField()
    pw_hash = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

#Classes for the post and likes
class PostManager(models.Manager):
    def verify(self,postData,id):
        if len(postData['post_secret']) < 4:
            return (False,'Post was too short')
        else:
            return (True, Post.objects.create(content=postData['post_secret'], creator=User.objects.get(id=id)))

    def like_post(self,user_id,post_id):
        post = self.get(id=post_id)
        liker = User.objects.get(id=user_id)
        user_likes = User.objects.filter(likes=post, id=user_id)
        if len(user_likes) != 0:
            return(False, "You have already liked this post")
        else:
            post.like.add(liker)
            return (True)



class Post(models.Model):
    content = models.TextField(max_length=1000)
    creator = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(User, related_name='likes')

    objects = PostManager()

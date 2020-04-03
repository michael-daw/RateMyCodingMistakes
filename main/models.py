from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from datetime import datetime
import enum

#Model storing the categories posts can be registered as
class Category(models.Model):
    
    NAME_MAX_LENGTH = 128
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True, primary_key=True)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
    
#Model for each post made on the site
class Post(models.Model):

    TITLE_MAX_LENGTH = 32
    POST_MAX_LENGTH = 240
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    body = models.CharField(max_length=POST_MAX_LENGTH)
    op = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images', blank=True)
    date = models.DateTimeField(default=datetime.now)
    rating = models.IntegerField(default=0)
    slug = models.SlugField(primary_key=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'posts'
    
    def __str__(self):
        return self.body
        
#Model stub for the comment system - not implemented
class Comment(models.Model):
    pass

#Model extending the default user class adding an experience level
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    STUDENT = 'STU'
    PROFESSIONAL = 'PRO'
    HOBBYIST = 'HOB'
    
    ExpChoice = [(STUDENT, 'Student'),(PROFESSIONAL, 'Professional'),(HOBBYIST,'Hobbyist')]
    experience = models.CharField(max_length=3, choices=ExpChoice, default=STUDENT)
    
    def __str__(self):
        return self.user.username

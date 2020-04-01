from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from datetime import datetime
import enum

class Category(models.Model):
    
    NAME_MAX_LENGTH = 128
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
    
class Post(models.Model):

    TITLE_MAX_LENGTH = 128
    POST_MAX_LENGTH = 1280
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    body = models.CharField(max_length=TITLE_MAX_LENGTH)
    op = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images', blank=True)
    date = models.DateTimeField(default=datetime.now)
    rating = models.IntegerField(default=0)
    
    def __str__(self):
        return self.body
        
class Comment(models.Model):
    pass #Add time

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    #subclass enum for choice of two experience types - student and professional
    class ExpChoice(enum.Enum):
        STUDENT = 'STU'
        PROFESSIONAL = 'PRO'
    
    experience = models.CharField(max_length=3, choices=[(tag, tag.value) for tag in ExpChoice])
    
    def __str__(self):
        return self.user.username

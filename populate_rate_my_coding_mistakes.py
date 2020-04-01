import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RateMyCodingMistakes.settings')

import django
django.setup()
from main.models import Category, Post, UserProfile
from django.contrib.auth.models import User

def populate():
    user = add_user(User.objects.create_user(username='test_user'))
    
    python_posts = [
        {'title': 'post #1 python',
         'body': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
         'rating': 60,
         'op':user},
        {'title':'post #2 python',
         'body':'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
         'rating': 100,
         'op':user},
        {'title':'post #3 python',
         'body':'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
         'rating': 15,
         'op':user}]
    
    java_posts = [
        {'title':'post #1 java',
        'body':'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
         'rating': 60,
         'op':user},
        {'title':'post #2 java',
         'body':'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
         'rating': 64,
         'op':user},
        {'title':'post #3 java',
         'body':'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
         'rating': 90,
         'op':user}]
             
    webdesign_posts = [
        {'title':'post #1 webdev',
         'body':'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
         'rating': 10,
         'op':user},
        {'title':'post #2 webdev',
         'body':'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
         'rating': 110,
         'op':user}]
         
    categories = {'Python': {'posts': python_posts},
            'Java': {'posts': java_posts},
            'Web Design': {'posts': webdesign_posts}}

    for cat, cat_data in categories.items():
        c = add_category(cat)
        for p in cat_data['posts']:
                add_post(c, p['title'], p['body'], p['op'], p['rating'])

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_post(cat,title,body,op,rating=0):
    p = Post.objects.get_or_create(category=cat, title=title, body=body, rating=rating, op=op)[0]
    p.save()
    return p
    
def add_category(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c

def add_user(username):
    u = UserProfile.objects.get_or_create(user=username)[0]
    u.save()
    return u

if __name__ == '__main__':
    print('Starting Rate My Coding Mistakes population script...')
    populate()


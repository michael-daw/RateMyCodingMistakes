import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rate_my_coding_mistakes.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
    python_posts = [
        {'title': 'post #1 python',
         'body': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
         'rating': 60},
        {'title':'post #2 python',
         'body':'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
         'rating': 100},
        {'title':'post #3 python',
         'body':'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
         'rating': 15}]
    
    java_posts = [
        {'title':'post #1 java',
            'body':'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
             'rating': 60},
            {'title':'post #2 java',
             'body':'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
             'rating': 64},
            {'title':'post #3 java',
             'body':'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
             'rating': 90}]
             
    webdesign_pages = [
        {'title':'post #1 webdev',
         'body':'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
         'rating': 10},
        {'title':'post #2 webdev',
         'body':'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
         'rating': 110}]
         
    categories = {'Python': {'posts': python_posts},
            'Java': {'posts': java_posts},
            'Web Design': {'posts': webdesign_posts}}

    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for p in cat_data['posts']:
                add_page(c, p['title'], p['body'], p['rating'])

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_post(cat,title,body,rating=0):
    p = Post.objects.get_or_create(category=cat, title=title)[0]
    p.body=body
    p.rating=rating
    p.save()
    return p
    
def add_category(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c

if __name__ == '__main__':
    print('Starting Rate My Coding Mistakes population script...')
    populate()


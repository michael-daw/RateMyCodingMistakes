from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    response = render(request, 'main/home.html')
    return response
    
def about(request):
    response = render(request, 'main/about.html')
    return response
    
def contact(request):
    response = render(request, 'main/contact.html')
    return response
    
def base(request):
    response = render(request, 'main/base.html')
    return response

@login_required
def account(request):
    response = render(request, 'main/account.html')
    return response
    
def login(request):
    response = render(request, 'main/login.html')
    return response

def register(request):
    response = render(request, 'main/signup.html')
    return response
    
def hot(request):
    context_dict = {'category':'Hot'}
    response = render(request, 'main/category.html', context=context_dict)
    return response

def alltime(request):
    context_dict = {'category':'All Time'}
    response = render(request, 'main/category.html', context=context_dict)
    return response

def new(request):
    context_dict = {'category':'New'}
    response = render(request, 'main/category.html', context=context_dict)
    return response
    
def categories(request):
    response = render(request, 'main/categories.html')
    return response
    
def sitemap(request):
    response = render(request, 'main/sitemap.html')
    return response
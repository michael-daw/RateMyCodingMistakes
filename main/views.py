from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from main.forms import UserForm, UserProfileForm, PostForm
from main.models import Post, Category, UserProfile
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime, timedelta

# Create your views here.
def home(request):
    post_list = Post.objects.order_by('-rating')
    context_dict = {}
    context_dict['posts'] = post_list
    
    visitor_cookie_handler(request)
    
    response = render(request, 'main/home.html', context_dict)
    return response
   
'''
Following functions deal with basic webpages - ie no models need accessed, only html page needs displayed
'''
   
def about(request):
    response = render(request, 'main/about.html')
    return response
    
def contact(request):
    response = render(request, 'main/contact.html')
    return response
    
def sitemap(request):
    response = render(request, 'main/sitemap.html')
    return response

'''
Following functions deal with user authentication and actions
'''

@login_required
def account(request):
    context_dict = {}
    try:
        logged_in_user = request.user
        posts = Post.objects.filter(op=logged_in_user).order_by('-date')
        context_dict['posts'] = posts
        
    except Post.DoesNotExist:
        context_dict['posts'] = None
        
    response = render(request, 'main/account.html', context_dict)
    return response
 
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('main:home'))
            else:
                return HttpResponse("Your RMCM account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'main/login.html')
    
@login_required
def user_logout(request):
    logout(request)
    response = render(request, 'main/home.html')
    return response

@login_required
def new_post(request):
    posted = False
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        
        if post_form.is_valid():
            post = post_form.save(commit = False)
            post.op = request.user
            post.save()
            posted=True
        else:
            print(post_form.errors)
    else:
        post_form = PostForm()
        
    context_dict = {}
    context_dict['post_form'] = post_form
    context_dict['posted'] = posted
    
    response = render(request, 'main/newpost.html', context_dict)
    return response
    

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    context_dict={}
    context_dict['user_form'] = user_form
    context_dict['profile_form'] =  profile_form
    context_dict['registered'] = registered
    
    response = render(request, 'main/signup.html', context_dict)
    return response

'''
Following 3 functions deal with displaying a subset of posts depending on which style
alltime shows highest rated posts
new shows more recently made posts
hot shows highest rated posts over a period of 2 days
'''

def hot(request):
    post_list = Post.objects.filter(date__range=[datetime.now()-timedelta(days=2), datetime.now()]).order_by('-rating')[:10]
    context_dict = {'category':'Hot', 'posts':post_list}
    response = render(request, 'main/category.html', context=context_dict)
    return response

def alltime(request):
    post_list = Post.objects.order_by('-rating')[:10]
    context_dict = {'category':'All Time', 'posts':post_list}
    response = render(request, 'main/category.html', context=context_dict)
    return response

def new(request):
    post_list = Post.objects.order_by('-date')[:10]
    context_dict = {'category':'New', 'posts':post_list}
    response = render(request, 'main/category.html', context=context_dict)
    return response
    
'''
Following functions deal with showing a list of categories the posts 
may be, and then displaying a list of posts in that category
'''

def show_categories(request):
    category_list = Category.objects.order_by('name')
    post_list = Post.objects.order_by('-rating')[:3]
            
    context_dict = {}
    context_dict['categories'] = category_list
    context_dict['posts'] = post_list
    
    visitor_cookie_handler(request)

    response = render(request, 'main/categories.html', context_dict)
    return response

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        posts = Post.objects.filter(category=category)
        context_dict['posts'] = posts
        context_dict['category'] = category
        
    except Category.DoesNotExist:
        context_dict['posts'] = None
        context_dict['category'] = None
        
    response = render(request, 'main/category.html', context_dict)
    return response
    
'''
Function to display a full post
'''
def show_post(request, category_name_slug, post_slug):
    context_dict = {}
    try:
        post = Post.objects.get(slug=post_slug)
        context_dict['post'] = post
    except Post.DoesNotExist:
        context_dict['post'] = None
        
    response = render(request, 'main/post.html', context_dict)
    return response
 
'''
Following functions deal with cookie handling
'''

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
    '%Y-%m-%d %H:%M:%S')
    
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
        
    request.session['visits'] = visits


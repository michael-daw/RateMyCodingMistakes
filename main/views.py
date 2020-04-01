from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rateMyCodingMistakes.models import Post, Category
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.
def home(request):
    post_list = Post.object.order_by('-rating')
    context_dict = {}
    context_dict['posts'] = post_list
    
    visitor_cookie_handler(request)
    
    response = render(request, 'main/home.html', context_dict)
    return response
    
def about(request):
    context_dict = {}
    context_dict['boldmessage'] = 'A place where programmers of all levels can collectively face-palm'
    response = render(request, 'main/about.html', context_dict)
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
 
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rateMyCodingMistakes:index'))
            else:
                return HttpResponse("Your RMCM account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rateMyCodingMistakes/login.html')
    
    response = render(request, 'main/login.html')
    return response
    
@login_required
def user_logout(request):
    logout(request)
    response = render(request, 'main/home.html')
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
    
    context_dict['user_form'] = user_form
    context_dict['profile_form'] =  profile_form
    context_dict['registered'] = registered
    
    response = render(request, 'main/signup.html', context_dict)
    return response

'''''''''''''''
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
 '''''''''''''''
def show_categories(request):
    category_list = Category.objects.order_by(name)
    post_list = Post.objects.order_by('-rating')[:3]
            
    context_dict = {}
    context_dict['categories'] = category_list
    context_dict['posts'] = post_list
    
    visitor_cookie_handler(request)

    response = render(request, 'main/categories.html', context_dict)
    return response

def show_category(request):
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
    
def sitemap(request):
    response = render(request, 'main/sitemap.html')
    return response

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


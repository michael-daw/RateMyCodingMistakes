from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('base/', views.base, name='base'),
    path('account/', views.account, name='account'),
    path('account/login/', views.login, name='login'),
    path('account/signup/', views.register, name='register'),
    path('hot/', views.hot, name='hot'),
    path('new/', views.new, name='new'),
    path('alltime/', views.alltime, name='alltime'),
    path('categories/', views.categories, name='categories'),
    path('sitemap/', views.sitemap, name='sitemap'),
]
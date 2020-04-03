from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('account/', views.account, name='account'),
    path('account/login/', views.user_login, name='login'),
    path('account/signup/', views.register, name='register'),
    path('account/logout/', views.user_logout, name='logout'),
    path('account/new_post', views.new_post, name='new_post'),
    path('hot/', views.hot, name='hot'),
    path('new/', views.new, name='new'),
    path('alltime/', views.alltime, name='alltime'),
    path('categories/', views.show_categories, name='categories'),
    path('categories/<slug:category_name_slug>', views.show_category, name='show_category'),
    path('categories/<slug:category_name_slug>/<slug:post_slug>', views.show_post, name='show_post'),
    path('sitemap/', views.sitemap, name='sitemap'),
]
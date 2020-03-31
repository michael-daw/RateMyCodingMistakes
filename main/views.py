from django.shortcuts import render

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
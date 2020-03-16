from django.shortcuts import render

# Create your views here.
def home(request):
    response = render(request, 'main/home.html')
    return response
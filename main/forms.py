from django import forms
from main.models import Post, Category, UserProfile
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('experience',)
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('op','date','rating','slug',)

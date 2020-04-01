from django.contrib import admin
from main.models import Category, Post, UserProfile

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'image')
    
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(UserProfile)


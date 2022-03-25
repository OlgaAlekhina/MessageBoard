from django.contrib import admin
from .models import Category, Post, Reply


class PostAdmin(admin.ModelAdmin):
    list_display = ('post_author', 'post_title', 'post_text', 'post_category', 'post_time')


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Reply)

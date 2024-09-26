from django.contrib import admin

from blog.models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'published_sign', 'title', 'content', 'image')

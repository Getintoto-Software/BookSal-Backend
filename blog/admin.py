from django.contrib import admin
from .models import Category, BlogPost
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at')
    search_fields = ('title', 'category__name', 'author')
    list_filter = ('category', 'created_at')
    ordering = ('-created_at',)

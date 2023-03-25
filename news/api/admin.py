from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Comment, News, User


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'text', 'published')
    search_fields = ('author',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'


class NewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author', 'likes', 'published')
    search_fields = ('title', 'author',)
    list_filter = ('title', 'author')
    empty_value_display = '-пусто-'


admin.site.register(Comment, CommentAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(User, UserAdmin)

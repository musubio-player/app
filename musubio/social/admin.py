from django.contrib import admin

from social.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'date_published', 'is_published')

admin.site.register(Comment, CommentAdmin)
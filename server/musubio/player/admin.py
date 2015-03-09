from django.contrib import admin

from player.models import Post, Room

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'youtube_id', 'user')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['initial'] = request.user.id

        return super(PostAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

class RoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['initial'] = request.user.id

        return super(RoomAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

admin.site.register(Post, PostAdmin)
admin.site.register(Room, RoomAdmin)
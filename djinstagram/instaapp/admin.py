from django.contrib import admin

# Register your models here.
from .models import Photo, Like, Tag, Follow

class PhotoAdmin(admin.ModelAdmin):
    '''
        Admin View for Photo
    '''
    list_display = ('owner', 'caption', 'created')

class FollowAdmin(admin.ModelAdmin):
    '''
        Admin View for Follow
    '''
    list_display = ('follower', 'following', 'active', 'created')

admin.site.register(Photo, PhotoAdmin)
admin.site.register(Follow, FollowAdmin)

admin.site.register(Like)
admin.site.register(Tag)

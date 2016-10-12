from django.contrib import admin

# Register your models here.
from .models import Photo, Like, Tag, Follow, Member, Comment

class CommentAdmin(admin.ModelAdmin):
    '''
        Admin View for Comment
    '''
    list_display = ('owner', 'photo', 'text')

class PhotoAdmin(admin.ModelAdmin):
    '''
        Admin View for Photo
    '''
    list_display = ('owner', 'caption', 'created', 'image_tag')
    readonly_fields = ('image_tag',)

class FollowAdmin(admin.ModelAdmin):
    '''
        Admin View for Follow
    '''
    list_display = ('follower', 'following', 'active', 'created')

class LikeAdmin(admin.ModelAdmin):
    '''
        Admin View for Like
    '''
    list_display = ('owner', 'image_tag')
    readonly_fields = ('image_tag',)

admin.site.register(Like, LikeAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Comment, CommentAdmin)

admin.site.register(Tag)
admin.site.register(Member)

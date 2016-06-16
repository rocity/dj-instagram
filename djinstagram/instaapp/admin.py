from django.contrib import admin

# Register your models here.
from .models import Photo, Like, Tag

class PhotoAdmin(admin.ModelAdmin):
    '''
        Admin View for Photo
    '''
    list_display = ('owner', 'caption', 'created')

admin.site.register(Photo, PhotoAdmin)
admin.site.register(Like)
admin.site.register(Tag)

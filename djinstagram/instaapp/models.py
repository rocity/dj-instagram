from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Tag(models.Model):
    name = models.TextField(max_length=255)

    def __str__(self):
        return self.name

class Photo(models.Model):
    owner = models.ForeignKey(User, null=True)
    caption = models.TextField(max_length=255)
    image = models.ImageField(null=True)
    tags = models.ManyToManyField(Tag)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image

class Like(models.Model):
    owner = models.ForeignKey(User, null=True)
    photo = models.ForeignKey(Photo, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.photo

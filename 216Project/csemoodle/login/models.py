# Create your models here.
from django.db import models


class PostImage(models.Model):
    postid = models.IntegerField()
    image = models.ImageField(upload_to = "Post")

    def __str__(self):
        return str(self.postid) + ' created'
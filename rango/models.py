from distutils.errors import LinkError
from msilib.schema import Class
from operator import mod
from django import urls, views
from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    

    # create Meta class for correcting typo
    class Meta:
        verbose_name_plural = 'Categories'

    # __str__() is simlar with toString() in Java
    def __str__(self):
        return self.name


class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


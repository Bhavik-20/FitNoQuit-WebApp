from pyexpat import model
from unicodedata import category
from django.db import models

# Create your models here.

class Blogs(models.Model):
    blog_id = models.PositiveIntegerField(primary_key= True)
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    publish_date = models.DateField()
    content = models.TextField()
    img = models.ImageField(upload_to='blog_images/')
    excerpt = models.TextField()
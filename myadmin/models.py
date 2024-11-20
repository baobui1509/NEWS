from django.db import models
from tinymce.models import HTMLField
from myadmin.define import *
from myadmin.helpers import *
from django.urls import reverse
from django.utils.timezone import now
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    is_homepage = models.BooleanField(default=False)
    status = models.CharField(max_length=15, choices=CATEGORY_STATUS_CHOICES, default=CATEGORY_STATUS_DEFAULT)
    layout = models.CharField(max_length=15, choices=CATEGORY_LAYOUT_CHOICES, default=CATEGORY_LAYOUT_DEFAULT)
    # image = models.ImageField(upload_to=get_file_path)
    
class Tag (models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)


class Article(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    is_homepage = models.BooleanField(default=False)
    status = models.CharField(max_length=15, choices=ARTICLE_STATUS_CHOICES, default=ARTICLE_STATUS_DEFAULT)
    ordering = models.IntegerField(default=0)
    special = models.BooleanField(default=False)
    publish_date = models.DateTimeField()
    content = HTMLField()
    image = models.ImageField(upload_to=get_file_path)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("article", kwargs={"article_slug": self.slug, 'article_id': self.id})
    
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    phone = PhoneNumberField(region='VN')
    created = models.DateTimeField(default=now)
    status = models.CharField(max_length=17, choices=CONTACT_STATUS_CHOICES, default=CONTACT_STATUS_DEFAULT)
    message = models.CharField(max_length=500)
    admin_message = models.TextField(max_length=500, default='', blank=True)
        
    def __str__(self):
        return self.name
    


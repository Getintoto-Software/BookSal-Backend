from django.db import models
from autoslug import AutoSlugField
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.
class Category(models.Model):
    id = AutoSlugField(primary_key=True, populate_from='name', unique=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    id = AutoSlugField(primary_key=True, populate_from='title', unique=True)
    meta_tags = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.CharField(max_length=255, blank=True, null=True)

    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='posts')
    content = CKEditor5Field(config_name='extends', blank=True, null=True)
    author = models.CharField(max_length=255)
    featured_status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

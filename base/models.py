from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.name

class Document(models.Model):
    name = models.CharField(max_length=300, null=True)
    slug = models.SlugField(max_length=500, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    document = models.FileField('documents/pdf')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='document_like')
    downloads = models.ManyToManyField(User, related_name='document_download')

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

    def number_of_likes(self):
        return self.likes.count()

    def number_of_downloads(self):
        return self.downloads.count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)
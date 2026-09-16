from django.db import models
from django.utils.text import slugify


class Post(models.Model):
    status_choices = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, unique=True)
    content = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=status_choices,
        default='published'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

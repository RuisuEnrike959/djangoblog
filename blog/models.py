from django.db import models
from django.contrib.auth.models import User


STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):

    author = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='posts',
    null=True,
    blank=True
)

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    cover_image = models.ImageField(
        upload_to='post_images/',
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    tags = models.ManyToManyField(
        Tag,
        blank=True
    )

    def __str__(self):
        return self.title
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts')
    tags = models.ManyToManyField(Tag, through='PostTag', blank=True)

    def __str__(self):
        return self.title


class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'tag')

    def __str__(self):
        return f"{self.post.title} - {self.tag.name}"


class Image(models.Model):
    post = models.ForeignKey(
        Post,
        related_name='images',
        on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='post_images/')

    def __str__(self):
        return f"Image for {self.post.title} ({self.image_file.url})"


class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes')
    post = models.ForeignKey(
        Post,
        related_name='liked_by',
        on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Ensures that each user can like a specific post only once."""
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"

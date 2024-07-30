from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """Model to extend the default Django User model with additional data."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username

#It is best to isolate logic for subscriptions in a separate model
class Subscription(models.Model):
    """Model to represent user subscriptions (followers and followees). M:M"""
    subscriber = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    subscribed_to = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscriber', 'subscribed_to')

    def __str__(self):
        return f"{self.subscriber.username} follows {self.subscribed_to.username}"

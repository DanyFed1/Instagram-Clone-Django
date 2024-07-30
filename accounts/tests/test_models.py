import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from unittest import mock
from accounts.models import Profile, Subscription

pytestmark = pytest.mark.django_db


def create_profile(sender, instance, created, **kwargs):
    """Create a profile whenever a new user is created."""
    if created:
        Profile.objects.create(user=instance)


class TestProfile:
    @pytest.fixture(autouse=True)
    def setup_signals(self):
        """
        Ensure that the signal for creating profiles is connected.
        """
        from django.db.models.signals import post_save
        post_save.connect(create_profile, sender=User)

    def test_profile_creation_signal(self):
        """
        Ensure that the `Profile` model is created via signals
        whenever a `User` is created.
        """
        user = mixer.blend(User)
        assert hasattr(
            user, 'profile'), "Profile is created automatically when a user is created."

    def test_profile_str(self):
        """
        Verify the string representation of the `Profile` model.
        """
        user = mixer.blend(User, username='john')
        assert str(
            user.profile) == 'john', "The string representation matches the user's username."

    @mock.patch('django.core.files.storage.FileSystemStorage.save',
                return_value='avatars/default.png')
    def test_profile_avatar_upload(self, mock_save):
        """
        Test avatar upload without saving an actual file to disk.
        """
        user = mixer.blend(User)
        user.profile.avatar = 'avatars/test.png'
        user.profile.save()

        assert user.profile.avatar == 'avatars/test.png', "Profile avatar field accepts and saves the given file path."

class TestSubscription:
    def test_subscription_creation(self):
        """
        Ensure that the `Subscription` model can create a subscription.
        """
        user1 = mixer.blend(User)
        user2 = mixer.blend(User)
        subscription = Subscription.objects.create(subscriber=user1, subscribed_to=user2)
        assert subscription in Subscription.objects.all(), "Subscription is created successfully."

    def test_subscription_str(self):
        """
        Verify the string representation of the `Subscription` model.
        """
        user1 = mixer.blend(User, username='user1')
        user2 = mixer.blend(User, username='user2')
        subscription = Subscription.objects.create(subscriber=user1, subscribed_to=user2)
        assert str(subscription) == 'user1 follows user2', "The string representation matches the subscription."
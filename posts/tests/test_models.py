import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from unittest import mock
from accounts.models import Profile
from posts.models import Tag, Post, PostTag, Image, Like

pytestmark = pytest.mark.django_db


def create_profile(sender, instance, created, **kwargs):
    """Create a profile whenever a new user is created."""
    if created:
        Profile.objects.create(user=instance)


class TestProfile:
    @pytest.fixture(autouse=True)
    def setup_signals(self):
        """Ensure that the signal for creating profiles is connected."""
        from django.db.models.signals import post_save
        post_save.connect(create_profile, sender=User)

    def test_profile_creation_signal(self):
        """Ensure that the Profile model is created via signals whenever a User is created."""
        user = mixer.blend(User)
        assert hasattr(
            user, 'profile'), "Profile is created automatically when a user is created."

    def test_profile_str(self):
        """Verify the string representation of the Profile model."""
        user = mixer.blend(User, username='john')
        assert str(
            user.profile) == 'john', "The string representation matches the user's username."

    @mock.patch('django.core.files.storage.FileSystemStorage.save',
                return_value='avatars/default.png')
    def test_profile_avatar_upload(self, mock_save):
        """Test avatar upload without saving an actual file to disk."""
        user = mixer.blend(User)
        user.profile.avatar = 'avatars/test.png'
        user.profile.save()

        assert user.profile.avatar == 'avatars/test.png', "Profile avatar field accepts and saves the given file path."


class TestTag:
    def test_tag_str(self):
        """Test the string representation of the Tag model."""
        tag = mixer.blend(Tag, name='Django')
        assert str(
            tag) == 'Django', "Tag string representation should match the tag name."

    def test_tag_unique_name(self):
        """Ensure that Tag names are unique."""
        tag1 = mixer.blend(Tag, name='UniqueTag')
        with pytest.raises(Exception):
            mixer.blend(Tag, name='UniqueTag')


class TestPost:
    def test_post_creation_with_tags(self):
        """Test the creation of a Post with tags."""
        tag1 = mixer.blend(Tag, name='Python')
        tag2 = mixer.blend(Tag, name='Django')

        # Create the post first
        post = mixer.blend(Post)

        # Assign tags using the many-to-many add method
        post.tags.add(tag1, tag2)

        # Ensure that the post is linked to both tags
        assert post.tags.count() == 2, "Post should be associated with two tags."


class TestPostTag:
    def test_post_tag_str(self):
        """Test the string representation of the PostTag model."""
        post = mixer.blend(Post, title='Tagged Post')
        tag = mixer.blend(Tag, name='Web Development')
        post_tag = mixer.blend(PostTag, post=post, tag=tag)

        assert str(
            post_tag) == 'Tagged Post - Web Development', "PostTag string representation should match the format 'Post Title - Tag Name'."


class TestImage:
    @mock.patch('django.core.files.storage.FileSystemStorage.save',
                return_value='post_images/test.png')
    def test_image_str(self, mock_save):
        """Test the string representation of the Image model without saving a file."""
        post = mixer.blend(Post, title='Image Post')
        image = mixer.blend(
            Image,
            post=post,
            image_file='post_images/test.png')

        # Mock the `url` method that returns the image file URL
        with mock.patch('django.db.models.fields.files.FieldFile.url', new_callable=mock.PropertyMock) as mock_url:
            mock_url.return_value = 'post_images/test.png'
            assert str(image) == 'Image for Image Post (post_images/test.png)', "Image string representation should match the format 'Image for Post Title (image path)'."


class TestLike:
    def test_like_str(self):
        """Test the string representation of the Like model."""
        user = mixer.blend(User, username='janedoe')
        post = mixer.blend(Post, title='Liked Post')
        like = mixer.blend(Like, user=user, post=post)

        assert str(
            like) == 'janedoe likes Liked Post', "Like string representation should match the format 'User likes Post'."

    def test_like_unique(self):
        """Ensure that each user can like a post only once."""
        user = mixer.blend(User)
        post = mixer.blend(Post)
        mixer.blend(Like, user=user, post=post)

        with pytest.raises(Exception):
            mixer.blend(Like, user=user, post=post)

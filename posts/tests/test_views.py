import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from model_bakery import baker
from posts.models import Post, Like
from accounts.models import Subscription


@pytest.mark.django_db
class TestPostViews:
    def setup_method(self):
        """Set up the test client and force authentication."""
        self.client = Client()
        self.user = User.objects.create(
            username='testuser', password='TestPassword123!')
        self.client.force_login(self.user)

    @pytest.mark.parametrize("method", ['get', 'post'])
    def test_post_create_view(self, method):
        """Test the post create view for both GET and POST requests."""
        if method == 'post':
            post_data = {'title': 'New Post', 'content': 'Test content'}
            response = self.client.post(
                reverse('posts:post_create'), data=post_data)
            assert response.status_code == 200, "Should redirect after successful post creation."
        else:
            response = self.client.get(reverse('posts:post_create'))
            assert response.status_code == 200, "Should render the post creation page."

    def test_post_detail_view(self):
        """Test the post detail view."""
        post = baker.make(Post, author=self.user)
        response = self.client.get(
            reverse(
                'posts:post_detail',
                kwargs={
                    'pk': post.pk}))
        assert response.status_code == 200, "Post detail page should render successfully."

    def test_feed_view(self):
        """Test the feed view."""
        response = self.client.get(reverse('posts:feed'))
        assert response.status_code == 200, "Feed page should render successfully."

    def test_friends_feed_view(self):
        """Test the friends feed view."""
        user2 = baker.make(User)
        post = baker.make(Post, author=user2)
        baker.make(Subscription, subscriber=self.user, subscribed_to=user2)

        response = self.client.get(reverse('posts:friends_feed'))
        assert response.status_code == 200, "Friends feed page should render successfully."
        assert post in response.context['posts'], "Post from subscribed user should be in the friends feed."


    def test_toggle_like_view(self):
        """Test the toggle like view."""
        post = baker.make(Post, author=self.user)
        like_url = reverse('posts:post_like', kwargs={'pk': post.pk})

        # Adding like
        response = self.client.post(like_url)
        assert response.status_code == 200, "Toggle like should return a JSON response."
        assert Like.objects.filter(
            user=self.user, post=post).exists(), "Like should be added."

        # Removing like
        response = self.client.post(like_url)
        assert response.status_code == 200, "Toggle like should still return a JSON response."
        assert not Like.objects.filter(
            user=self.user, post=post).exists(), "Like should be removed."

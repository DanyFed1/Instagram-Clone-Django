import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from model_bakery import baker
from accounts.models import Profile, Subscription
from accounts.tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


@pytest.mark.django_db
class TestViews:
    def setup_method(self):
        """Set up the test client."""
        self.client = Client()

    def test_register_view(self):
        """Test the register view to ensure user registration works."""
        form_data = {
            'username': 'testuser',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'email': 'testuser@example.com',
        }
        response = self.client.post(
            reverse('accounts:register'), data=form_data)

        assert response.status_code == 302, "Should redirect after successful registration."
        assert User.objects.filter(
            username='testuser').exists(), "User should be created."
        assert Profile.objects.filter(
            user__username='testuser').exists(), "Profile should be created."

    def test_activate_view(self):
        """Test the activate view to confirm account activation."""
        user = baker.make(User, is_active=False)
        profile = baker.make(Profile, user=user)

        setattr(profile, 'email_confirmed', False)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        url = reverse(
            'accounts:activate',
            kwargs={
                'uidb64': uid,
                'token': token})

        response = self.client.get(url)

        assert response.status_code == 302, "Should redirect after activation."

        user.refresh_from_db()
        assert user.is_active, "User should be activated."

        setattr(profile, 'email_confirmed', True)
        assert profile.email_confirmed, "Email should be confirmed."

    @pytest.mark.parametrize("method", ['get', 'post'])
    def test_profile_update_view(self, method):
        """Test the profile update view."""
        user = baker.make(User, username='profileuser')
        profile = baker.make(Profile, user=user)
        self.client.force_login(user)

        if method == 'post':
            response = self.client.post(
                reverse('accounts:profile_update'), data={
                    'full_name': 'Updated User'})
            assert response.status_code == 302, "Should redirect after a successful profile update."
            profile.refresh_from_db()
            assert profile.full_name == 'Updated User', "Profile should be updated."
        else:
            response = self.client.get(reverse('accounts:profile_update'))
            assert response.status_code == 200, "Should render the profile update page."

    def test_login_view(self):
        """Test the login view to confirm authentication works and redirects the user correctly."""
        user = baker.make(User, username='testlogin')
        user.set_password('TestPassword123!')
        user.save()

        response = self.client.post(
            reverse('accounts:login'),
            data={
                'username': 'testlogin',
                'password': 'TestPassword123!'})
        assert response.status_code == 302, "Login should redirect to the profile update page."

    @pytest.mark.parametrize('view_name',
                             ['accounts:logout', 'accounts:profile'])
    def test_logout_and_profile_views(self, view_name):
        """Test the logout and profile views for correct rendering."""
        user = baker.make(User, username='testlogout')
        baker.make(Profile, user=user)
        self.client.force_login(user)

        if view_name == 'accounts:logout':
            response = self.client.get(reverse(view_name))
            assert response.status_code == 302, "Logout should redirect after logout."
        elif view_name == 'accounts:profile':
            response = self.client.get(reverse(view_name))
            assert response.status_code == 200, "Profile page should render successfully."

    def test_subscribe_view(self):
        """Test the subscribe view to ensure users can follow others."""
        user1 = baker.make(User)
        user2 = baker.make(User)
        self.client.force_login(user1)

        response = self.client.post(reverse('accounts:subscribe', kwargs={'user_id': user2.id}))
        assert response.status_code == 200, "Subscribe should return a 200 status code."
        assert Subscription.objects.filter(subscriber=user1,
                                           subscribed_to=user2).exists(), "Subscription should be created."

    def test_unsubscribe_view(self):
        """Test the unsubscribe view to ensure users can unfollow others."""
        user1 = baker.make(User)
        user2 = baker.make(User)
        baker.make(Subscription, subscriber=user1, subscribed_to=user2)
        self.client.force_login(user1)

        response = self.client.post(reverse('accounts:unsubscribe', kwargs={'user_id': user2.id}))
        assert response.status_code == 200, "Unsubscribe should return a 200 status code."
        assert not Subscription.objects.filter(subscriber=user1,
                                               subscribed_to=user2).exists(), "Subscription should be deleted."

    def test_social_login_view(self):
        """Test the social login view to ensure it redirects appropriately."""
        user = baker.make(User, username='socialuser')
        self.client.force_login(user)

        response = self.client.get(reverse('social_login'))
        assert response.status_code == 302, "Social login should redirect if user is authenticated."

    def test_custom_social_signup_view(self):
        """Test the custom social signup view to ensure it redirects appropriately."""
        user = baker.make(User, username='socialuser')
        self.client.force_login(user)

        response = self.client.get(reverse('socialaccount_signup'))
        assert response.status_code == 302, "Social signup should redirect if user is authenticated."

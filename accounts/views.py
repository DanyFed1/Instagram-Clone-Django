from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm
from .models import Profile, Subscription
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.http import JsonResponse
from allauth.socialaccount.views import SignupView
from allauth.socialaccount.models import SocialLogin
from django.contrib.auth import get_backends


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User will be activated after email confirmation
            user.save()

            # Check if profile already exists
            if not Profile.objects.filter(user=user).exists():
                # Explicitly create a user profile if it doesn't exist
                Profile.objects.create(user=user)

            # Domain setting for activation link
            current_site_domain = "127.0.0.1:8000" #For local
            # current_site_domain = "djangogram-pet-projec.lm.r.appspot.com" #For deployment
            subject = 'Activate Your DjangoGram Account'
            message = render_to_string(
                'accounts/account_activation_email.html',
                {
                    'user': user,
                    'domain': current_site_domain,
                    'uid': urlsafe_base64_encode(
                        force_bytes(
                            user.pk)),
                    'token': account_activation_token.make_token(user),
                })
            user.email_user(subject, message)
            return redirect('accounts:account_activation_sent')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})



def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        if not Profile.objects.filter(user=user).exists():
            Profile.objects.create(user=user)  # Ensure profile creation
        user.save()

        # Get the first available backend
        backend = get_backends()[0]
        user.backend = f'{backend.__module__}.{backend.__class__.__name__}'

        login(request, user, backend=user.backend)
        return redirect('accounts:profile_update')
    else:
        return render(request, 'accounts/account_activation_invalid.html')


@login_required
def profile_update(request):
    """Allows users to update their profile information. It requires users to be logged in."""
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'accounts/profile_update.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile_update')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                if not hasattr(user, 'profile'):
                    Profile.objects.create(user=user)  # Ensure profile creation
                login(request, user)
                return redirect('accounts:profile_update')
            else:
                messages.error(request, "Username or password is incorrect.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})



def logout_view(request):
    """Logout Functionality"""
    logout(request)
    return redirect('accounts:profile')


def account_activation_sent(request):
    """Displays a page informing the user that an activation email has been sent."""
    return render(request, 'accounts/account_activation_sent.html')


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})


#Subscribtion logic:
@login_required
def subscribe(request, user_id):
    subscribed_to = get_object_or_404(User, id=user_id)
    Subscription.objects.get_or_create(subscriber=request.user, subscribed_to=subscribed_to)
    return JsonResponse({'status': 'subscribed'}, status=200)

@login_required
def unsubscribe(request, user_id):
    subscribed_to = get_object_or_404(User, id=user_id)
    Subscription.objects.filter(subscriber=request.user, subscribed_to=subscribed_to).delete()
    return JsonResponse({'status': 'unsubscribed'}, status=200)

class CustomSocialSignupView(SignupView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:profile_update')
        else:
            return super().dispatch(request, *args, **kwargs)

def social_login(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile_update')

    return redirect('socialaccount_signup')


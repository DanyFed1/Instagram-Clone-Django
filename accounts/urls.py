from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('profile/', views.profile, name='profile'),
    path('subscribe/<int:user_id>/', views.subscribe, name='subscribe'),
    path('unsubscribe/<int:user_id>/', views.unsubscribe, name='unsubscribe'),
    path('social/login/', views.social_login, name='social_login'),
]


from django.utils.deprecation import MiddlewareMixin
from .models import Profile

class EnsureProfileMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            if not hasattr(request.user, 'profile'):
                Profile.objects.get_or_create(user=request.user)

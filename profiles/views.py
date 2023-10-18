
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .serializers import CookieTokenRefreshSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from django.views import View
from django.http import JsonResponse
class CookieTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14  # 14 days
            response.set_cookie(
                'refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True)
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14  # 14 days
            response.set_cookie(
                'refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True)
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)

class LogoutView(View):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get('refresh_token')
        if token:
            try:
                token_obj = OutstandingToken.objects.get(token=token)
                token_obj.blacklisted = True
                token_obj.save()
                response = JsonResponse({'success': 'logout successful'})
                response.delete_cookie('refresh_token')
                return response
            except OutstandingToken.DoesNotExist:
                pass
        return JsonResponse({'error': 'logout failed'}, status=400)

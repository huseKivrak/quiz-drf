from django.urls import path, include
from profiles.views import CookieTokenObtainPairView, CookieTokenRefreshView, LogoutView

app_name = 'api'

urlpatterns = [
    path('', include('quizzes.urls')),
    path('auth/token/', CookieTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('auth/token/refresh/',
         CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
]

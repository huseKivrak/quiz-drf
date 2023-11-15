from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("quizzes.api.urls")),
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/signup/", include("dj_rest_auth.registration.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]

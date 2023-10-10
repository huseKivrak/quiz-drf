from django.urls import path
from quizzes.api import views as quiz_views

app_name='api'
urlpatterns = [
    # {% url 'api:quizzes' %}
    path(
        route='quizzes/',
        view=quiz_views.QuizListCreateAPIView.as_view(),
        name='quizzes'
    ),
    # {% url 'api:quiz' quiz.uuid %}
    path(
        route='quizzes/<uuid:uuid>/',
        view=quiz_views.QuizRetrieveUpdateDestroyAPIView.as_view(),
        name='quiz'
    ),
]
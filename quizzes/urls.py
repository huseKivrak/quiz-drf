from django.urls import path
from quizzes.api import views

urlpatterns = [
    # /quizzes/api/
    path(
        route='api/',
        view=views.QuizListCreateAPIView.as_view(),
        name='quiz_rest_api'
    ),
    # /quizzes/api/:uuid/
    path(
        route='api/<uuid:uuid>/',
        view=views.QuizRetrieveUpdateDestroyAPIView.as_view(),
        name='quiz_rest_api'
    )

]

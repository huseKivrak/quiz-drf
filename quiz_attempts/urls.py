from django.urls import path
from quiz_attempts.api import views

urlpatterns = [
    path(
        "quiz_attempts/",
        views.QuizAttemptListCreateAPIView.as_view(),
        name="quiz_attempt_list_create",
    ),
    path(
        "quiz_attempts/<int:pk>/",
        views.QuizAttemptRetrieveUpdateDestroyAPIView.as_view(),
        name="quiz_attempt_detail",
    ),
    # QuestionAttempt URLs
    path(
        "question_attempts/",
        views.QuestionAttemptListCreateAPIView.as_view(),
        name="question_attempt_list_create",
    ),
    path(
        "question_attempts/<int:pk>/",
        views.QuestionAttemptRetrieveUpdateDestroyAPIView.as_view(),
        name="question_attempt_detail",
    ),
]

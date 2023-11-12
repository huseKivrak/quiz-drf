from django.urls import path
from quizzes.api import views

urlpatterns = [
    # Quiz URLs
    path("quizzes/", views.QuizListCreateAPIView.as_view(), name="quiz_list_create"),
    path(
        "quizzes/<slug:slug>/",
        views.QuizRetrieveUpdateDestroyAPIView.as_view(),
        name="quiz_detail",
    ),
    # Question URLs
    # path(
    #     "questions/",
    #     views.QuestionListCreateAPIView.as_view(),
    #     name="question_list_create",
    # ),
    # path(
    #     "questions/<slug:slug>/",
    #     views.QuestionRetrieveUpdateDestroyAPIView.as_view(),
    #     name="question_detail",
    # ),
    # Answer URLs
    path(
        "answers/", views.AnswerListCreateAPIView.as_view(), name="answer_list_create"
    ),
    path(
        "answers/<slug:slug>/",
        views.AnswerRetrieveUpdateDestroyAPIView.as_view(),
        name="answer_detail",
    ),
    # QuizAttempt URLs
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

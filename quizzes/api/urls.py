from django.urls import path
from . import views

urlpatterns = [
    # Quiz URLs
    path("quizzes/", views.QuizListCreateAPIView.as_view(), name="quiz_list_create"),
    path(
        "quizzes/<slug:slug>/",
        views.QuizRetrieveUpdateDestroyAPIView.as_view(),
        name="quiz_detail",
    ),
    path(
        "quizzes/<slug:quiz_slug>/questions/<int:question_id>/",
        views.QuestionDetailView.as_view(),
        name="question_detail",
    ),
    path(
        "answers/", views.AnswerListCreateAPIView.as_view(), name="answer_list_create"
    ),
    path(
        "answers/<slug:slug>/",
        views.AnswerRetrieveUpdateDestroyAPIView.as_view(),
        name="answer_detail",
    ),
]

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly, SAFE_METHODS
from ..models import Quiz, Question, Answer
from .serializers import QuizSerializer, QuestionSerializer, AnswerSerializer


class IsAuthorOrReadOnly(BasePermission):
    """
    Custom permission to only allow the author of an object to edit or delete it.
    # todo: utilize built-in DRF permission for this (Django Object Permissions)
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


# Quiz Views:
class QuizListCreateAPIView(ListCreateAPIView):
    """
    List all quizzes, or create a new quiz.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    lookup_field = 'slug'


class QuizRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a quiz instance.
    """
    permission_classes = (IsAuthorOrReadOnly,)

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    lookup_field = 'slug'


# Question Views:
class QuestionListCreateAPIView(ListCreateAPIView):
    """
    List all questions, or create a new question.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'slug'


class QuestionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a question instance.
    """
    permission_classes = (IsAuthorOrReadOnly,)

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'slug'

# Answer Views:
class AnswerListCreateAPIView(ListCreateAPIView):
    """
    List all answers, or create a new answer.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    lookup_field = 'slug'


class AnswerRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a answer instance.
    """
    permission_classes = (IsAuthorOrReadOnly,)

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    lookup_field = 'slug'

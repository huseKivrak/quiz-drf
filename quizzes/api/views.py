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


class QuizListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    lookup_field = 'slug'


class QuizRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    lookup_field = 'slug'


class QuestionListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'slug'


class QuestionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'slug'


class AnswerListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    lookup_field = 'slug'


class AnswerRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    lookup_field = 'slug'

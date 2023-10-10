from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from rest_framework.permissions import IsAuthenticated

from ..models import Quiz, Question, Answer
from .serializers import QuizSerializer, QuestionSerializer, AnswerSerializer


class QuizListCreateAPIView(ListCreateAPIView):
    queryset = Quiz.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = QuizSerializer
    lookup_field = 'uuid'


class QuizRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = QuizSerializer
    lookup_field = 'uuid'


class QuestionListCreateAPIView(ListCreateAPIView):
    queryset = Question.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionSerializer
    lookup_field = 'uuid'


class QuestionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionSerializer
    lookup_field = 'uuid'


class AnswerListCreateAPIView(ListCreateAPIView):
    queryset = Answer.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = AnswerSerializer
    lookup_field = 'uuid'


class AnswerRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = AnswerSerializer
    lookup_field = 'uuid'

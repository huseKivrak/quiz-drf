from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404
)

from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly, SAFE_METHODS
from ..models import Quiz, Question, Answer, QuizAttempt, QuestionAttempt
from .serializers import QuizSerializer, QuestionSerializer, AnswerSerializer, QuizAttemptSerializer, QuestionAttemptSerializer
from django.db.models import Prefetch


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

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quiz = serializer.save(author=request.user)

        # Create nested Questions
        questions_data = serializer.validated_data.get('questions', [])
        for order, question_data in enumerate(questions_data, start=0):
            question = Question.objects.create(
                quiz=quiz,
                text=question_data['text'],
                question_type=question_data['question_type'],
                order=order,
                author=request.user
            )

            answers_data = question_data.get('answers', [])

            for order, answer_data in enumerate(answers_data, start=0):
                Answer.objects.create(
                    question=question,
                    text=answer_data['text'],
                    is_correct=answer_data['is_correct'],
                    order=order,
                )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


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


class QuestionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a question instance.
    """
    permission_classes = (IsAuthorOrReadOnly,)

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

# Answer Views:


class AnswerListCreateAPIView(ListCreateAPIView):
    """
    List all answers, or create a new answer.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class AnswerRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a answer instance.
    """
    permission_classes = (IsAuthorOrReadOnly,)

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

# QuizAttempt Views


class QuizAttemptListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = QuizAttemptSerializer

    def get_queryset(self):
        return QuizAttempt.objects.filter(user=self.request.user).prefetch_related(
            Prefetch('question_attempts',
                     queryset=QuestionAttempt.objects.all())
        )

    def create(self, request, *args, **kwargs):
        user = request.user
        quiz_id = request.data.get('quiz')

        quiz = get_object_or_404(Quiz, id=quiz_id)
        quiz_attempt = QuizAttempt.objects.create(user=user, quiz=quiz)

        serializer = QuizAttemptSerializer(quiz_attempt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# QuestionAttempt Views
class QuestionAttemptListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = QuestionAttemptSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        quiz_attempt_id = request.data.get('quiz_attempt')
        question_id = request.data.get('question')
        answer_id = request.data.get('answer_selected')

        quiz_attempt = get_object_or_404(
            QuizAttempt, id=quiz_attempt_id, user=user)
        question = Question.objects.get(id=question_id)
        answer = Answer.objects.get(id=answer_id)

        question_attempt = QuestionAttempt.objects.create(
            quiz_attempt=quiz_attempt,
            question=question,
            answer_selected=answer,
            is_correct=(answer.is_correct)
        )

        serializer = QuestionAttemptSerializer(question_attempt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QuizAttemptRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = QuizAttempt.objects.all()
    serializer_class = QuizAttemptSerializer


class QuestionAttemptRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = QuestionAttempt.objects.all()
    serializer_class = QuestionAttemptSerializer

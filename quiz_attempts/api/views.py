from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from serializers import (
    QuizAttemptSerializer,
    QuestionAttemptSerializer,
)
from ..models import (
    QuizAttempt,
    QuestionAttempt,
)

from quizzes.models import (
    Quiz,
    Question,
    Answer,
)

from quizzes.api.views import IsAuthorOrReadOnly


class QuizAttemptListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = QuizAttemptSerializer

    def get_queryset(self):
        return QuizAttempt.objects.filter(user=self.request.user).prefetch_related(
            Prefetch("question_attempts", queryset=QuestionAttempt.objects.all())
        )

    def create(self, request, *args, **kwargs):
        user = request.user
        quiz_id = request.data.get("quiz")

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
        quiz_attempt_id = request.data.get("quiz_attempt")
        question_id = request.data.get("question")
        answer_id = request.data.get("answer_selected")

        quiz_attempt = get_object_or_404(QuizAttempt, id=quiz_attempt_id, user=user)
        question = Question.objects.get(id=question_id)
        answer = Answer.objects.get(id=answer_id)

        question_attempt = QuestionAttempt.objects.create(
            quiz_attempt=quiz_attempt,
            question=question,
            answer_selected=answer,
            is_correct=(answer.is_correct),
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

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly, SAFE_METHODS
from ..models import Quiz, Question, Answer, QuizAttempt, QuestionAttempt
from .serializers import QuizSerializer, QuestionSerializer, AnswerSerializer, QuizAttemptSerializer, QuestionAttemptSerializer


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

# QuizAttempt Views
class QuizAttemptListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = QuizAttempt.objects.all()
    serializer_class = QuizAttemptSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        quiz_id = request.data.get('quiz')
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)

        quiz_attempt = QuizAttempt.objects.create(user=user, quiz=quiz)
        serializer = QuizAttemptSerializer(quiz_attempt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# QuestionAttempt Views
class QuestionAttemptListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = QuestionAttempt.objects.all()
    serializer_class = QuestionAttemptSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        quiz_attempt_id = request.data.get('quiz_attempt')
        question_id = request.data.get('question')
        answer_id = request.data.get('answer_selected')

        try:
            quiz_attempt = QuizAttempt.objects.get(id=quiz_attempt_id, user=user)
            question = Question.objects.get(id=question_id)
            answer = Answer.objects.get(id=answer_id)
        except (QuizAttempt.DoesNotExist, Question.DoesNotExist, Answer.DoesNotExist):
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        question_attempt = QuestionAttempt.objects.create(
            quiz_attempt=quiz_attempt,
            question=question,
            answer_selected=answer,
            is_correct=(answer.is_correct)
        )
        serializer = QuestionAttemptSerializer(question_attempt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

from model_utils.models import TimeStampedModel
from django.db import models
from profiles.models import User
from quizzes.models import Quiz, Question, Answer


class QuizAttempt(TimeStampedModel):
    user = models.ForeignKey(
        User, related_name="quiz_attempts", on_delete=models.CASCADE
    )
    quiz = models.ForeignKey(Quiz, related_name="attempts", on_delete=models.CASCADE)
    completed = models.DateTimeField(blank=True, null=True)
    score = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ["user", "quiz", "created"]


class QuestionAttempt(TimeStampedModel):
    question = models.ForeignKey(
        Question, related_name="attempts", on_delete=models.CASCADE
    )
    quiz_attempt = models.ForeignKey(
        QuizAttempt, related_name="question_attempts", on_delete=models.CASCADE
    )
    answer_selected = models.ForeignKey(
        Answer, related_name="selections", on_delete=models.CASCADE
    )
    time_taken = models.DurationField(null=True, blank=True)

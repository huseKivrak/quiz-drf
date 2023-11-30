from autoslug import AutoSlugField
from django.db import models
from model_utils.models import (
    TimeStampedModel,
    StatusModel,
    UUIDModel,
)
from model_utils import FieldTracker, Choices
from profiles.models import User


# Quiz Model:
class Quiz(TimeStampedModel, StatusModel, UUIDModel):
    STATUS = Choices("draft", "published")

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    slug = AutoSlugField(populate_from="title", unique=True)

    author = models.ForeignKey(
        User, related_name="user_quizzes", on_delete=models.SET_NULL, null=True
    )

    tracker = FieldTracker()

    class Meta:
        ordering = ["-created"]
        unique_together = ["title", "author"]

    def __str__(self):
        return self.title


class Question(TimeStampedModel, UUIDModel):
    """
    Question model for quizzes.
    """

    QUESTION_TYPES = Choices(
        ("true_false", "True/False"),
        ("multiple_choice", "Multiple Choice"),
    )

    question_text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=30, choices=QUESTION_TYPES)
    order = models.PositiveIntegerField(default=1)
    quiz = models.ForeignKey(
        Quiz, related_name="quiz_questions", on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        User, related_name="user_questions", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        ordering = ["order"]
        unique_together = ["quiz", "order"]

    def __str__(self):
        return f"{self.quiz.title} - Q#{self.order}"


# Answer model
class Answer(TimeStampedModel, UUIDModel):
    """
    Answer model for questions.
    """

    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=1)
    question = models.ForeignKey(
        Question, related_name="question_answers", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["order"]
        unique_together = ["question", "order"]

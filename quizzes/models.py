from autoslug import AutoSlugField
from django.db import models
from model_utils.models import (
    TimeStampedModel,
    StatusModel,
    UUIDModel,
)
from model_utils import FieldTracker, Choices
from polymorphic.models import PolymorphicModel
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


class Question(
    PolymorphicModel,
    TimeStampedModel,
    UUIDModel,
):
    """
    Question model that defines common fields and methods for
    all question types.
    """

    question_text = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=1)
    quiz = models.ForeignKey(
        Quiz, related_name="quiz_questions", on_delete=models.SET_NULL, null=True
    )
    author = models.ForeignKey(
        User, related_name="user_questions", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.quiz.title} - Q#{self.order}"


class TrueFalseQuestion(Question):
    """
    Question type that has a true or false answer.
    """

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super(TrueFalseQuestion, self).save(*args, **kwargs)

        if is_new:
            Answer.objects.create(answer_text="True", question=self)
            Answer.objects.create(answer_text="False", question=self)


class MultipleChoiceQuestion(Question):
    """
    Question type that has multiple choices as answers.
    """


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

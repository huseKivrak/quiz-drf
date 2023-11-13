import uuid as uuid_lib
from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse

from core.models import TimeStampedModel
from profiles.models import User


# Quiz Model:
class Quiz(TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    slug = AutoSlugField(populate_from="title", unique=True)
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    is_published = models.BooleanField(default=False)

    author = models.ForeignKey(
        User, related_name="user_quizzes", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        ordering = ["-created"]
        unique_together = ["title", "author"]

    def get_absolute_url(self):
        return reverse("quizzes:detail", kwargs={"slug": self.slug})


class Question(TimeStampedModel):
    """
    Abstract Question model that defines common fields and methods for
    all question types.
    """

    question_text = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="text", unique=True)
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)

    order = models.PositiveIntegerField(default=1)

    quiz = models.ForeignKey(
        Quiz, related_name="quiz_questions", on_delete=models.SET_NULL, null=True
    )

    author = models.ForeignKey(
        User, related_name="user_questions", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        ordering = ["order"]

    # def get_slug(self):
    #     return self.text + "-" + str(self.order)


class TrueFalseQuestion(Question):
    """
    Question type that has a true or false answer.
    """

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super(TrueFalseQuestion, self).save(*args, **kwargs)

        if is_new:
            Answer.objects.create(text="True", question=self)
            Answer.objects.create(text="False", question=self)


class MultipleChoiceQuestion(Question):
    """
    Question type that has multiple choices as answers.
    """


# Answer model
class Answer(TimeStampedModel):
    """
    Answer model for questions.
    """

    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    order = models.PositiveIntegerField(default=1)
    question = models.ForeignKey(
        Question, related_name="question_answers", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["order"]
        unique_together = ["question", "order"]


###################################################
###################################################
###################################################


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

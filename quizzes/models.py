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
        User, related_name="quizzes", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        ordering = ["-created"]
        unique_together = ["title", "author"]

    def get_absolute_url(self):
        return reverse("quizzes:detail", kwargs={"slug": self.slug})


# Question Model:
class Question(TimeStampedModel):
    class QuestionType(models.TextChoices):
        MULTIPLE_CHOICE = "multiple_choice", "Multiple Choice"
        TRUE_FALSE = "true_false", "True/False"

    text = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="text", unique=True)
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)

    question_type = models.CharField(
        max_length=50,
        choices=QuestionType.choices,
        default=QuestionType.MULTIPLE_CHOICE,
    )

    order = models.PositiveIntegerField(default=1)

    quiz = models.ForeignKey(
        Quiz, related_name="questions", on_delete=models.SET_NULL, null=True
    )

    author = models.ForeignKey(
        User, related_name="questions", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        ordering = ["order"]
        unique_together = ["quiz", "order"]

    def get_absolute_url(self):
        return reverse("quizzes:question_detail", kwargs={"slug": self.slug})

    # def save(self, *args, **kwargs):
    #     """
    #     Create 'True' and 'False' answers for new True/False questions
    #     """

    #     super(Question, self).save(*args, **kwargs)

        # if not self.pk and self.question_type == self.QuestionType.TRUE_FALSE:
        #     Answer.objects.create(
        #         text='True',
        #         question=self)
        #     Answer.objects.create(
        #         text='False',
        #         question=self)


# Answer model
class Answer(TimeStampedModel):
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)

    def get_slug(self):
        return self.question.slug + "-" + str(self.order)

    slug = AutoSlugField(populate_from=get_slug, unique=True)

    order = models.PositiveIntegerField(default=1)

    question = models.ForeignKey(
        Question, related_name="answers", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["order"]
        unique_together = ["question", "order"]


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

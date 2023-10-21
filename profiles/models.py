
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

DEFAULT_AVATAR = 'avatars/default.png'


# User Model:
class User(AbstractUser):
    class Types(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        TEACHER = 'TEACHER', 'Teacher'

    # ? Two Scoops: 'Ensures that creating new users through proxy models works'
    base_type = Types.STUDENT

    # type of User:
    type = models.CharField(
        # ! Two Scoops: _('Type') here
        max_length=50, choices=Types.choices, default=Types.STUDENT)

    avatar = models.ImageField(
        upload_to='avatars/', blank=True, default=DEFAULT_AVATAR)

    def save(self, *args, **kwargs):
        # If a new user, set the user's type based off the base_type property
        if not self.pk:
            self.type = self.base_type

        return super().save(*args, **kwargs)


# Student Proxy Model:
class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(type=User.Types.STUDENT)


class Student(User):
    base_type = User.Types.STUDENT

    objects = StudentManager()

    class Meta:
        proxy = True


# Teacher Proxy Model:
class TeacherManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(type=User.Types.TEACHER)


class Teacher(User):
    base_type = User.Types.TEACHER

    objects = TeacherManager()

    class Meta:
        proxy = True

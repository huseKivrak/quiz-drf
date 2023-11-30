from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from model_utils import Choices


# User Model:
class User(AbstractUser):
    TYPES = Choices("teacher", "student")

    user_type = models.CharField(max_length=7, choices=TYPES, default=TYPES.teacher)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


# Teacher Proxy Model:
class TeacherManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(user_type=User.TYPES.teacher)


class Teacher(User):
    objects = TeacherManager()

    class Meta:
        proxy = True


# Student Proxy Model:
class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(user_type=User.TYPES.student)


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True

from rest_framework import serializers
from profiles.serializers import UserSerializer
from ..models import (
    Quiz,
    Question,
    Answer,
)


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            "id",
            "answer_text",
            "is_correct",
        ]


class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for questions, independant of quiz creation.
    """

    question_answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "question_text",
            "question_type",
            "order",
            "quiz",
            "question_answers",
        ]

    def validate_question_answers(self, value):
        """
        Custom validation for answers based on question type.
        """
        if self.initial_data["question_type"] == "true_false":
            if not (
                len(value) == 2 and sum(answer["is_correct"] for answer in value) == 1
            ):
                raise serializers.ValidationError(
                    "True/False questions must have 1 correct answer & 2 total answers."
                )

        elif self.initial_data["question_type"] == "multiple_choice":
            if len(value) < 2 or sum(answer["is_correct"] for answer in value) != 1:
                raise serializers.ValidationError(
                    "Multiple choice must have 1 correct answer and at least 2 total."
                )


class QuizSerializer(serializers.ModelSerializer):
    quiz_questions = QuestionSerializer(many=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Quiz
        fields = [
            "id",
            "title",
            "description",
            "quiz_questions",
            "slug",
            "author",
            "status",
            "created",
            "modified",
        ]

    def validate(self, data):
        """
        Validate that quizzes have at least one question before publishing.
        """
        if data.get("status", "published") and not data.get("quiz_questions"):
            raise serializers.ValidationError(
                "Quizzes must have at least one question before publishing."
            )

        return data

    def create(self, validated_data):
        questions_data = validated_data.pop("quiz_questions", [])
        quiz = Quiz.objects.create(**validated_data)
        for question in questions_data:
            answers_data = question.pop("question_answers", [])
            Question.objects.create(quiz=quiz, **question)
            for answer in answers_data:
                Answer.objects.create(question=question, **answers_data)
        return quiz

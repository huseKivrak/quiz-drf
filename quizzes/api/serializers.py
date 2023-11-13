from rest_framework import serializers
from ..models import (
    Quiz,
    Question,
    TrueFalseQuestion,
    MultipleChoiceQuestion,
    Answer,
    QuizAttempt,
    QuestionAttempt,
)


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            "pk",
            "question",
            "answer_text",
            "is_correct",
            "uuid",
            "order",
            "created",
            "modified",
        ]


class TrueFalseQuestionSerializer(serializers.ModelSerializer):
    correct_answer = serializers.CharField(write_only=True)

    class Meta:
        model = TrueFalseQuestion
        fields = [
            "pk",
            "order",
            "quiz",
            "correct_answer",
            "question_text",
            "slug",
            "author",
            "uuid",
            "created",
            "modified",
        ]

    def create(self, validated_data):
        correct_answer = validated_data.pop("correct_answer")
        question = super().create(validated_data)

        if correct_answer == "true":
            question.question_answers.filter(text="True").update(is_correct=True)
        elif correct_answer == "false":
            question.question_answers.filter(text="False").update(is_correct=True)

        return question

    def validate_correct_answer(self, value):
        if value not in ["true", "false"]:
            raise serializers.ValidationError(
                "Correct answer must be 'true' or 'false'."
            )
        return value


class MultipleChoiceQuestionSerializer(serializers.ModelSerializer):
    question_answers = AnswerSerializer(many=True, required=True)

    class Meta:
        model = MultipleChoiceQuestion
        fields = [
            "pk",
            "order",
            "quiz",
            "question_text",
            "question_answers",
            "slug",
            "author",
            "uuid",
            "created",
            "modified",
        ]

    def validate_question_answers(self, value):
        """
        Check that exactly one answer is marked correct.
        """
        correct_answer_count = sum(answer.get("is_correct", False) for answer in value)
        if correct_answer_count != 1:
            raise serializers.ValidationError(
                "Exactly one answer must be marked correct."
            )
        return value

    def create(self, validated_data):
        answers_data = validated_data.pop("question_answers")
        question = super().create(validated_data)
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)
        return question


class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for questions, independant of quiz creation.
    """

    question_type = serializers.CharField(write_only=True)
    question_answers = AnswerSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = [
            "pk",
            "order",
            "quiz",
            "question_type",
            "question_text",
            "question_answers",
            "slug",
            "author",
            "uuid",
            "created",
            "modified",
        ]

    def create(self, validated_data):
        question_type = validated_data.pop("question_type")

        if question_type == "multiple_choice":
            question = MultipleChoiceQuestion.objects.create(**validated_data)
        elif question_type == "true_false":
            question = TrueFalseQuestion.objects.create(**validated_data)

        return question

    def to_representation(self, instance):
        if isinstance(instance, TrueFalseQuestion):
            return TrueFalseQuestionSerializer(instance=instance).data
        elif isinstance(instance, MultipleChoiceQuestion):
            return MultipleChoiceQuestionSerializer(instance=instance).data
        return super().to_representation(instance)

    def validate_question_answers(self, value):
        if self.initial_data["question_type"] == "multiple_choice" and len(value) < 2:
            raise serializers.ValidationError(
                "Multiple choice questions must have at least two answers."
            )
        return value


class QuizSerializer(serializers.ModelSerializer):
    quiz_questions = QuestionSerializer(many=True, required=True)
    author = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = [
            "pk",
            "title",
            "description",
            "slug",
            "quiz_questions",
            "is_published",
            "author",
            "uuid",
            "created",
            "modified",
        ]

    def get_author(self, obj):
        return obj.author.username

    def validate(self, data):
        """
        Validate that quizzes have at least one question before publishing.
        """
        if data.get("is_published", True) and not data.get("quiz_questions"):
            raise serializers.ValidationError(
                "Quizzes must have at least one question before publishing."
            )

        return data

    def create(self, validated_data):
        question_data = validated_data.pop("quiz_questions")
        quiz = Quiz.objects.create(**validated_data)
        for question in question_data:
            Question.objects.create(quiz=quiz, **question)
        return quiz


##########################################
##########################################


class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = ["pk", "user", "quiz", "created", "modified", "completed", "score"]
        # read_only_fields = ['pk', 'user', 'quiz',
        #           'created', 'modified', 'completed', 'score']

    def create(self, validated_data):
        user = self.context["request"].user
        instance = QuizAttempt.objects.create(user=user, **validated_data)
        return instance


class QuestionAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAttempt
        fields = [
            "pk",
            "quiz_attempt",
            "question",
            "created",
            "modified",
            "answer_selected",
            "is_correct",
            "time_taken",
        ]
        # read_only_fields = ['pk', 'is_correct']

        def create(self, validated_data):
            instance = QuestionAttempt.objects.create(**validated_data)

            # updating score
            quiz_attempt = instance.quiz_attempt
            if instance.is_correct:
                quiz_attempt.score = (quiz_attempt.score or 0) + 1
                quiz_attempt.save()
            return instance

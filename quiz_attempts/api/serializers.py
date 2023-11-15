from rest_framework import serializers
from ..models import QuizAttempt, QuestionAttempt


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

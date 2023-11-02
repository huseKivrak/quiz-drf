from rest_framework import serializers
from ..models import Quiz, Question, Answer, QuizAttempt, QuestionAttempt


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'pk', 'question', 'text', 'is_correct', 'uuid', 'order',  'created', 'modified']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = [
            'pk', 'order', 'quiz', 'text', 'question_type', 'answers', 'slug',  'author',  'uuid', 'created', 'modified']

    def validate(self, data):
        """
        Validate multiple choice questions
        """
        if data['question_type'] == Question.QuestionType.MULTIPLE_CHOICE:
            answers = data.get('answers', [])

            if len(answers) < 2:
                raise serializers.ValidationError(
                    'Multiple choice questions must have at least two answers.')

            if not any(answer['is_correct'] for answer in answers):
                raise serializers.ValidationError(
                    "Multiple choice questions must have at least one correct answer.")

        return data


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Quiz
        fields = [
            'pk', 'title', 'description', 'slug', 'questions', 'is_published', 'author', 'uuid', 'created', 'modified']

    def validate(self, data):
        """
        Validate that quizzes have at least one question before publishing.
        """
        if data.get('is_published', True) and not data.get('questions'):
            raise serializers.ValidationError(
                'Quizzes must have at least one question before publishing.')

        return data

##########################################
##########################################


class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = ['pk', 'user', 'quiz',
                  'created', 'modified', 'completed', 'score']
        # read_only_fields = ['pk', 'user', 'quiz',
        #           'created', 'modified', 'completed', 'score']

    def create(self, validated_data):
        user = self.context['request'].user
        instance = QuizAttempt.objects.create(user=user, **validated_data)
        return instance


class QuestionAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAttempt
        fields = ['pk', 'quiz_attempt', 'question', 'created', 'modified',
                  'answer_selected', 'is_correct', 'time_taken',]
        # read_only_fields = ['pk', 'is_correct']

        def create(self, validated_data):
            instance = QuestionAttempt.objects.create(**validated_data)

            # updating score
            quiz_attempt = instance.quiz_attempt
            if instance.is_correct:
                quiz_attempt.score = (quiz_attempt.score or 0) + 1
                quiz_attempt.save()
            return instance

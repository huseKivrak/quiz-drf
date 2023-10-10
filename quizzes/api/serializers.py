from rest_framework import serializers
from ..models import Quiz, Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'text', 'is_correct', 'uuid', 'order', 'question']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = [
            'text', 'slug', 'uuid', 'question_type', 'order', 'quiz', 'author']

    def validate(self, data):
        """
        Validate multiple choice questions
        """
        if data['question_type'] == Question.QuestionType.MULTIPLE_CHOICE:
            answers = data.get('answers', [])

            if len(answers) < 2:
                raise serializers.ValidationError(
                    'Multiple choice questions must have at least one answer')

            if not any(answer['is_correct'] for answer in answers):
                raise serializers.ValidationError(
                    "Multiple choice questions must have at least one correct answer.")

        return data


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Quiz
        fields = [
            'title', 'description', 'slug', 'uuid', 'is_published', 'author', 'questions']

    def validate(self, data):
        """
        Validate that quizzes have at least one question before publishing.
        """
        if data.get('is_published', False) and not data.get('questions'):
            raise serializers.ValidationError(
                'Quizzes must have at least one question before publishing.')

        return data

from django.contrib import admin
from .models import TrueFalseQuestion, MultipleChoiceQuestion, Answer

admin.site.register(TrueFalseQuestion)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(Answer)

from django.contrib import admin

from question.models import Tag, Question, Answer, QuestionVote, AnswerVote

admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuestionVote)
admin.site.register(AnswerVote)

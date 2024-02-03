from django.views.generic import ListView

from question.models import Question


class QuestionListView(ListView):
    model = Question
    template_name = "question/index.html"

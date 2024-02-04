from django.shortcuts import render
from django.views.generic import ListView

from question.models import Question


class QuestionListView(ListView):
    model = Question
    template_name = "question/index.html"
    paginate_by = 20

    def post(self, request):
        filter_option = request.POST.get("filter_option")
        active_button = request.POST.get("filter_option", "option1")
        if filter_option == "option1":
            questions = Question.objects.order_by("-created_at")
        elif filter_option == "option2":
            questions = Question.objects.order_by("created_at")
        else:
            questions = Question.objects.all()
        context = {"question_list": questions, "active_button": active_button}
        return render(request, self.template_name, context)

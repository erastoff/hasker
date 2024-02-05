from django.shortcuts import render
from django.db.models import Count
from django.views.generic import ListView, CreateView, DetailView

from question.models import Question


class QuestionListView(ListView):
    model = Question
    template_name = "question/index.html"
    # context_object_name = "questions"
    paginate_by = 20

    def get_queryset(self):
        return Question.objects.annotate(num_answers=Count("answers"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request):
        filter_option = request.POST.get("filter_option")
        active_button = request.POST.get("filter_option", "option1")
        if filter_option == "option1":
            questions = Question.objects.order_by("-created_at").annotate(
                num_answers=Count("answers")
            )
        elif filter_option == "option2":
            questions = Question.objects.order_by("created_at").annotate(
                num_answers=Count("answers")
            )
        else:
            questions = Question.objects.annotate(num_answers=Count("answers"))
        context = {"question_list": questions, "active_button": active_button}
        return render(request, self.template_name, context)


class QuestionCreateView(CreateView):
    pass


class QuestionDetailView(DetailView):
    model = Question
    template_name = "question/detail.html"
    context_object_name = "question"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = context["question"]
        context["answers"] = question.answers.all()
        return context

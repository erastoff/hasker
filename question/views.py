from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from question.forms import QuestionCreateForm
from question.models import Question, Answer


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
            questions = Question.objects.order_by("-votes").annotate(
                num_answers=Count("answers")
            )
        else:
            questions = Question.objects.annotate(num_answers=Count("answers"))
        context = {"question_list": questions, "active_button": active_button}
        return render(request, self.template_name, context)


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    template_name = "question/add_question.html"
    form_class = QuestionCreateForm
    success_url = reverse_lazy("question:index")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class QuestionDetailView(DetailView):
    model = Question
    template_name = "question/detail.html"
    context_object_name = "question"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = context["question"]
        context["answers"] = question.answers.all().order_by("-is_right", "-votes")
        return context


class QuestionSearchView(ListView):
    model = Question
    template_name = "question/question_search.html"
    context_object_name = "search_results"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Question.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            ).annotate(num_answers=Count("answers"))
        return Question.objects.none()


class QuestionTagSearchView(ListView):
    model = Question
    template_name = "question/question_search.html"
    context_object_name = "search_tag_results"

    def get_queryset(self):
        tag_word = self.kwargs.get("tag_word")
        queryset = Question.objects.filter(tags__tag_word=tag_word).annotate(
            num_answers=Count("answers")
        )
        return queryset


def create_answer(request, pk):
    if request.method == "POST":
        print("request: ", request)
        print("request method: ", request.method)
        print("request text: ", request.POST.get("text_input"))
        Answer.objects.create(
            content=request.POST.get("text_input"),
            author=request.user,
            question=Question.objects.get(pk=pk),
        )
        return redirect("question:question_detail", pk=pk)


def incr_vote_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question.incr_vote()
    return JsonResponse({"votes": question.votes})


def decr_vote_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question.decr_vote()
    return JsonResponse({"votes": question.votes})


def incr_vote_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    answer.incr_vote()
    return JsonResponse({"votes": answer.votes})


def decr_vote_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    answer.decr_vote()
    return JsonResponse({"votes": answer.votes})

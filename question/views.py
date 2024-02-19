from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from question.forms import QuestionCreateForm
from question.models import Question, Answer, QuestionVote, AnswerVote


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
            # questions = random.sample(questions)
        context = {"question_list": questions, "active_button": active_button}
        return render(request, self.template_name, context)


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    template_name = "question/add_question.html"
    form_class = QuestionCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        created_object = self.object
        pk = created_object.pk
        success_url = reverse_lazy("question:question_detail", kwargs={"pk": pk})
        return success_url


class QuestionDetailView(DetailView):
    model = Question
    template_name = "question/detail.html"
    context_object_name = "question"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = context["question"]
        context["answers"] = question.answers.all().order_by(
            "-is_right", "-votes", "-created_at"
        )
        context["choose_right"] = False
        if context["answers"] and context["answers"].first().is_right != True:
            context["choose_right"] = True
        return context


class QuestionSearchView(ListView):
    model = Question
    template_name = "question/question_search.html"
    context_object_name = "search_results"
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return (
                Question.objects.filter(
                    Q(title__icontains=query) | Q(content__icontains=query)
                )
                .annotate(num_answers=Count("answers"))
                .order_by("-votes", "-created_at")
            )
        return Question.objects.none()


class QuestionTagSearchView(ListView):
    model = Question
    template_name = "question/question_search.html"
    context_object_name = "search_tag_results"
    paginate_by = 20

    def get_queryset(self):
        tag_word = self.kwargs.get("tag_word")
        queryset = (
            Question.objects.filter(tags__tag_word=tag_word)
            .annotate(num_answers=Count("answers"))
            .order_by("-votes", "-created_at")
        )
        return queryset


def create_answer(request, pk):
    if request.method == "POST":
        Answer.objects.create(
            content=request.POST.get("text_input"),
            author=request.user,
            question=Question.objects.get(pk=pk),
        )
        return redirect("question:question_detail", pk=pk)


def incr_vote_question(request, pk):
    question = Question.objects.prefetch_related("qvotes").get(pk=pk)
    q_vote = question.qvotes.first()
    if q_vote:
        if q_vote.vote_type != "+":
            q_vote.upvote()
            question.incr_vote()
    else:
        QuestionVote.objects.create(user=request.user, question_id=pk, vote_type="+")
        question.incr_vote()
    return JsonResponse({"votes": question.votes})


def decr_vote_question(request, pk):
    question = Question.objects.prefetch_related("qvotes").get(pk=pk)
    q_vote = question.qvotes.first()
    if q_vote:
        if q_vote.vote_type != "-":
            q_vote.downvote()
            question.decr_vote()
    else:
        QuestionVote.objects.create(user=request.user, question_id=pk, vote_type="-")
        question.decr_vote()
    return JsonResponse({"votes": question.votes})


def incr_vote_answer(request, pk):
    answer = Answer.objects.prefetch_related("avotes").get(pk=pk)
    a_vote = answer.avotes.first()
    if a_vote:
        if a_vote.vote_type != "+":
            a_vote.upvote()
            answer.incr_vote()
    else:
        AnswerVote.objects.create(user=request.user, answer_id=pk, vote_type="+")
        answer.incr_vote()
    return JsonResponse({"votes": answer.votes})


def decr_vote_answer(request, pk):
    answer = Answer.objects.prefetch_related("avotes").get(pk=pk)
    a_vote = answer.avotes.first()
    if a_vote:
        if a_vote.vote_type != "-":
            a_vote.downvote()
            answer.decr_vote()
    else:
        AnswerVote.objects.create(user=request.user, answer_id=pk, vote_type="-")
        answer.decr_vote()
    return JsonResponse({"votes": answer.votes})


def answer_is_right(request, question_pk, answer_pk):
    answer = Answer.objects.get(pk=answer_pk)
    answer.right()
    return redirect("question:question_detail", pk=question_pk)

from django.urls import path

from question.views import (
    QuestionListView,
    QuestionDetailView,
    QuestionCreateView,
    create_answer,
    QuestionSearchView,
    QuestionTagSearchView,
    incr_vote_question,
    decr_vote_question,
    decr_vote_answer,
    incr_vote_answer,
)

app_name = "question"

urlpatterns = [
    path("ask/", QuestionListView.as_view(), name="index"),
    path("question/<int:pk>/", QuestionDetailView.as_view(), name="question_detail"),
    path("ask/add/", QuestionCreateView.as_view(), name="question_create"),
    path("question/<int:pk>/add_answer/", create_answer, name="add_answer"),
    path("search/", QuestionSearchView.as_view(), name="question_search"),
    path(
        "tag/<str:tag_word>/",
        QuestionTagSearchView.as_view(),
        name="question_tag_search",
    ),
    path("question/<int:pk>/incr_vote/", incr_vote_question, name="incr_vote_question"),
    path(
        "question/<int:pk>/decr_vote/",
        decr_vote_question,
        name="decr_vote_question",
    ),
    path(
        "question/<int:pk>/incr_answer_vote/", incr_vote_answer, name="incr_vote_answer"
    ),
    path(
        "question/<int:pk>/decr_answer_vote/",
        decr_vote_answer,
        name="decr_vote_answer",
    ),
]

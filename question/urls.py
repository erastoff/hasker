from django.urls import path

from question.views import (
    QuestionListView,
    QuestionDetailView,
    QuestionCreateView,
    create_answer,
)

app_name = "question"

urlpatterns = [
    path("", QuestionListView.as_view(), name="index"),
    path("question/<int:pk>/", QuestionDetailView.as_view(), name="question_detail"),
    path("question/add/", QuestionCreateView.as_view(), name="question_create"),
    path("question/<int:pk>/add_answer/", create_answer, name="add_answer"),
]

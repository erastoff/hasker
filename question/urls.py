from django.urls import path

from question.views import QuestionListView, QuestionDetailView

app_name = "question"

urlpatterns = [
    path("", QuestionListView.as_view(), name="index"),
    path("question/<int:pk>/", QuestionDetailView.as_view(), name="question_detail"),
]

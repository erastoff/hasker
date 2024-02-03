from django.urls import path

from question.views import QuestionListView

app_name = "question"

urlpatterns = [
    path("", QuestionListView.as_view(), name="index"),
]

from django.urls import path

from api.views import QuestionListAPIView

app_name = "api"

urlpatterns = [
    path("question_list/", QuestionListAPIView.as_view(), name="question_list/"),
]

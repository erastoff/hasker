from django.urls import path

from api.views import QuestionListAPIView
from api.views import QuestionDetailAPIView

app_name = "api"

urlpatterns = [
    path("question_list/", QuestionListAPIView.as_view(), name="question-list"),
    path("question/<int:pk>/", QuestionDetailAPIView.as_view(), name="question-api"),
]

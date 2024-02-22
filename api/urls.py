from django.urls import path

from api.views import (
    QuestionListAPIView,
    QuestionSearchAPIView,
    QuestionDetailAPIView,
    QuestionTagSearchAPIView,
)

app_name = "api"

urlpatterns = [
    path("question_list/", QuestionListAPIView.as_view(), name="question-list"),
    path("question/<int:pk>/", QuestionDetailAPIView.as_view(), name="question-api"),
    path("search/", QuestionSearchAPIView.as_view(), name="question_search-api"),
    path(
        "tag/<str:tag_word>/",
        QuestionTagSearchAPIView.as_view(),
        name="question_tag_search_api",
    ),
]

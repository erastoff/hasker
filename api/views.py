from django.db.models import Q, Count
from rest_framework.generics import ListAPIView, RetrieveAPIView

from question.models import Question
from question.serializers import QuestionListSerializer, QuestionDetailSerializer


class QuestionListAPIView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionListSerializer


class QuestionDetailAPIView(RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionDetailSerializer
    lookup_field = "pk"


class QuestionSearchAPIView(ListAPIView):
    serializer_class = QuestionListSerializer

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


class QuestionTagSearchAPIView(ListAPIView):
    serializer_class = QuestionListSerializer

    def get_queryset(self):
        tag_word = self.kwargs.get("tag_word")
        queryset = (
            Question.objects.filter(tags__tag_word=tag_word)
            .annotate(num_answers=Count("answers"))
            .order_by("-votes", "-created_at")
        )
        return queryset

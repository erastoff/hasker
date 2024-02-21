from rest_framework.generics import ListAPIView, RetrieveAPIView

# from rest_framework.viewsets import ModelViewSet

from question.models import Question
from question.serializers import QuestionListSerializer, QuestionDetailSerializer


class QuestionListAPIView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionListSerializer


class QuestionDetailAPIView(RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionDetailSerializer
    lookup_field = "pk"

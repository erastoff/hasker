from rest_framework.generics import ListAPIView

# from rest_framework.viewsets import ModelViewSet

from question.models import Question
from question.serializers import QuestionSerializer


class QuestionListAPIView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

from .models import Question


def popular_questions(request):
    popular_questions = Question.objects.order_by("-votes")[:5]
    return {"popular_questions": popular_questions}

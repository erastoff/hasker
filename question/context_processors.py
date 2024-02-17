from .models import Question


def popular_questions(request):
    popular_questions = Question.objects.order_by("-votes", "-created_at")[:20]
    return {"popular_questions": popular_questions}

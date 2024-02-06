from django import forms
from django.forms import Widget

from question.models import Question


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = (
            "title",
            "content",
            # "author",
            "tags",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.items():
            print(field)
            widget: Widget = field[1].widget
            widget.attrs["class"] = "form-control"

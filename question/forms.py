from django import forms
from django.forms import widgets, Widget

from hasker.settings import DEBUG
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

            for name, field in self.fields.items():
                widget: Widget = field.widget
                widget.attrs["class"] = "form-control"
                if name == "created_at":
                    self.fields["created_at"].widget = widgets.DateInput(
                        attrs={
                            "type": "date",
                            "placeholder": "yyyy-mm-dd (DOB)",
                            "class": "form-control",
                        }
                    )
                if DEBUG:
                    print(name, field, field.widget)

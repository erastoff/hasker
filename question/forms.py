from django import forms
from django.db import transaction
from django.forms import Widget

from question.models import Question, Tag


class QuestionCreateForm(forms.ModelForm):
    tags = forms.CharField(label="Tags", max_length=100)

    class Meta:
        model = Question
        fields = (
            "title",
            "content",
            # "author",
            # "tags",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.items():
            print(field)
            widget: Widget = field[1].widget
            widget.attrs["class"] = "form-control"

    def clean_tags(self):
        tags_str = self.cleaned_data["tags"]
        tags_data = [tag.strip() for tag in tags_str.split(",") if tag.strip()]
        if len(tags_data) > 3:
            raise forms.ValidationError("You can't add more than 3 tags.")

        cleaned_tags = []
        with transaction.atomic():
            for tag_name in tags_data:
                tag, created = Tag.objects.get_or_create(tag_word=tag_name)
                cleaned_tags.append(tag)
        return cleaned_tags

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            instance.tags.add(*self.cleaned_data["tags"])
        return instance

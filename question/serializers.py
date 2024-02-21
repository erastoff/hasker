from rest_framework import serializers


from question.models import Question, Answer


class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    tags = serializers.SlugRelatedField(
        slug_field="tag_word", read_only=True, many=True
    )

    class Meta:
        model = Question
        fields = ("title", "content", "author", "created_at", "tags", "votes")

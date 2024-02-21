from rest_framework import serializers


from question.models import Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Answer
        fields = ("content", "author", "created_at", "is_right", "votes")


class QuestionDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    tags = serializers.SlugRelatedField(
        slug_field="tag_word", read_only=True, many=True
    )
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = (
            "title",
            "content",
            "author",
            "created_at",
            "tags",
            "votes",
            "answers",
        )


class QuestionListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    tags = serializers.SlugRelatedField(
        slug_field="tag_word", read_only=True, many=True
    )

    class Meta:
        model = Question
        fields = (
            "title",
            "content",
            "author",
            "created_at",
            "tags",
            "votes",
        )

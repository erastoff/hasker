from rest_framework import serializers


from question.models import Question, Answer, Tag


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


class TagListField(serializers.ListField):
    child = serializers.CharField(max_length=100)

    def to_representation(self, data):
        return [tag.tag_word for tag in data.all()]

    def to_internal_value(self, data):
        if isinstance(data, str):
            return [tag.strip() for tag in data.split(",")]
        elif isinstance(data, list):
            return data


class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    tags = TagListField()

    class Meta:
        model = Question
        fields = "__all__"

    def create(self, validated_data):
        tags_data = validated_data.pop("tags")
        question = Question.objects.create(**validated_data)
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(tag_word=tag_name)
            question.tags.add(tag)
        return question

from django.db import models

from users.models import User


class Tag(models.Model):
    tag_word = models.CharField(blank=False, null=False, max_length=30)

    def __str__(self):
        return self.tag_word


class Question(models.Model):
    title = models.CharField(max_length=120, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name="questions")
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def incr_vote(self):
        self.votes += 1
        self.save()

    def decr_vote(self):
        self.votes -= 1
        self.save()


class Answer(models.Model):
    content = models.TextField()
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_right = models.BooleanField(default=False)
    question = models.ForeignKey(
        to=Question, on_delete=models.CASCADE, related_name="answers"
    )
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"Question {self.question} Answer {self.pk}"

    def incr_vote(self):
        self.votes += 1
        self.save()

    def decr_vote(self):
        self.votes -= 1
        self.save()


class QuestionVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(
        Question, related_name="qvotes", on_delete=models.CASCADE
    )
    vote_type = models.CharField(
        max_length=1,
        choices=[("+", "Upvote"), ("0", "Unvoted"), ("-", "Downvote")],
        default="0",
    )

    class Meta:
        unique_together = [
            "user",
            "question",
        ]

    def __str__(self):
        return f"{self.user.username} voted {self.vote_type} for {self.question}"

    def upvote(self):
        if self.vote_type == "-":
            self.vote_type = "0"
        elif self.vote_type == "0":
            self.vote_type = "+"
        self.save()

    def downvote(self):
        if self.vote_type == "+":
            self.vote_type = "0"
        elif self.vote_type == "0":
            self.vote_type = "-"
        self.save()


class AnswerVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, related_name="avotes", on_delete=models.CASCADE)
    vote_type = models.CharField(
        max_length=1,
        choices=[("+", "Upvote"), ("0", "Unvoted"), ("-", "Downvote")],
        default="0",
    )

    class Meta:
        unique_together = [
            "user",
            "answer",
        ]

    def __str__(self):
        return f"{self.user.username} voted {self.vote_type} for {self.answer}"

    def upvote(self):
        if self.vote_type == "-":
            self.vote_type = "0"
        elif self.vote_type == "0":
            self.vote_type = "+"
        self.save()

    def downvote(self):
        if self.vote_type == "+":
            self.vote_type = "0"
        elif self.vote_type == "0":
            self.vote_type = "-"
        self.save()

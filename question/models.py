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

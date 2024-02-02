from django.db import IntegrityError
from django.test import TestCase
from datetime import datetime

from question.models import Tag, Question, Answer
from users.models import User


class QuestionModelTest(TestCase):

    TAG_WORD_1 = "django"
    TAG_WORD_2 = "python"
    QUESTION_TITLE = "python - django"
    QUESTION_CONTENT = "Python or django?"
    ANSWER_CONTENT = "I think django!"
    USER_USERNAME_1 = "testuser1"
    USER_EMAIL_1 = "test1@example.com"
    USER_PASSWORD_1 = "testpassword1"
    USER_USERNAME_2 = "testuser2"
    USER_EMAIL_2 = "test2@example.com"
    USER_PASSWORD_2 = "testpassword2"

    def setUp(self):
        self.user1 = User.objects.create(
            email=self.USER_EMAIL_1,
            username=self.USER_USERNAME_1,
            password=self.USER_PASSWORD_1,
        )
        self.user2 = User.objects.create(
            email=self.USER_EMAIL_2,
            username=self.USER_USERNAME_2,
            password=self.USER_PASSWORD_2,
        )
        self.tag1 = Tag.objects.create(tag_word=self.TAG_WORD_1)
        self.tag2 = Tag.objects.create(tag_word=self.TAG_WORD_2)
        self.question = Question.objects.create(
            title=self.QUESTION_TITLE,
            content=self.QUESTION_CONTENT,
            author=self.user1,
        )
        self.question.tags.set([self.tag1, self.tag2])
        self.answer = Answer.objects.create(
            content=self.ANSWER_CONTENT,
            author=self.user2,
            is_right=True,
            question=self.question,
        )

    def test_instance(self):
        self.assertEqual(self.question.title, self.QUESTION_TITLE)
        self.assertEqual(self.question.content, self.QUESTION_CONTENT)

    def test_unique_pk_enforced(self):
        """Test that two question with same pk are not allowed."""
        with self.assertRaises(IntegrityError):
            Question.objects.create(
                title=self.QUESTION_TITLE,
                content=self.QUESTION_CONTENT,
                author=self.user1,
                pk=1,
            )

    def test_added_date_automatically(self):
        """Test that the date is automatically saved on creation"""
        self.assertTrue(type(self.question.created_at), datetime)

    def test_str(self):
        """Test the __str__ method"""
        self.assertEqual(str(self.question), self.QUESTION_TITLE)

    def test_tag_values(self):
        self.assertEqual(str(self.tag1), self.TAG_WORD_1)
        self.assertEqual(str(self.tag2), self.TAG_WORD_2)

    def test_answer(self):
        self.assertTrue(self.answer.content, self.ANSWER_CONTENT)
        self.assertTrue(self.answer.author, self.user2)
        self.assertTrue(self.answer.author, self.user2)
        self.assertTrue(type(self.answer.created_at), datetime)
        self.assertTrue(type(self.answer.question), Question)

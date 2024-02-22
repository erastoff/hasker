from django.test import Client

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from question.models import Question, Tag
from users.models import User


class QuestionAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="12345"
        )
        self.token = Token.objects.create(user=self.user)
        # API client creation
        self.client = Client()

    def test_create_question(self):
        url = "/api/question/create/"
        data = {
            "title": "Test Question",
            "content": "This is a test question content",
            "tags": "test, question",
        }
        # users's Token to header Authorization
        headers = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}
        # sending POST query to create new question
        response = self.client.post(url, data, **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Question.objects.get().title, "Test Question")

    def test_get_question_detail(self):
        question = Question.objects.create(
            title="Test Question",
            author_id=self.user.pk,
            content="This is a test question content",
        )
        question.tags.add(Tag.objects.create(tag_word="test"))
        url = f"/api/question/{question.pk}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Question")

    def test_get_questions_list(self):
        Question.objects.create(
            title="Test Question 1",
            author=self.user,
            content="This is a test question content 1",
        )
        Question.objects.create(
            title="Test Question 2",
            author=self.user,
            content="This is a test question content 2",
        )
        url = "/api/question_list/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

from django.test import TestCase

from users.models import User


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create(
            email="test@example.com",
            username="testuser",
            password="testpassword",
        )

        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.username, "testuser")

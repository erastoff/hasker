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

    #     def test_slug_value(self):
    #         """
    #         Test that the slug is automatically added to the movie on creation.
    #         """
    #         expected = slugify(self.movie.title)
    #         actual = self.movie.slug
    #         self.assertEqual(expected, actual)
    #
    #     def test_slug_value_for_duplicate_title(self):
    #         """
    #         Test that two movies with identical titles get unique slugs.
    #         """
    #         movie2 = Movie.objects.create(
    #             title=self.movie.title, release_date=self.RELEASE_DATE, api_id=99
    #         )
    #
    #         self.assertNotEqual(self.movie.slug, movie2.slug)
    #
    def test_added_date_automatically(self):
        """Test that the date is automatically saved on creation"""
        self.assertTrue(type(self.question.created_at), datetime)

    #     def test_active_false_by_default(self):
    #         """Test that our booleans are set to false by default"""
    #         self.assertTrue(type(self.movie.active) == bool)
    #         self.assertFalse(self.movie.active)
    #
    #     def test_deleted_false_by_default(self):
    #         """Test that our booleans are set to false by default"""
    #         self.assertTrue(type(self.movie.deleted) == bool)
    #         self.assertFalse(self.movie.deleted)
    #
    def test_str(self):
        """Test the __str__ method"""
        self.assertEqual(str(self.question), self.QUESTION_TITLE)


#
# class TestGenre(TestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         cls.genre = Genre.objects.create(name="Western", api_id=1)
#
#     def test_has_name(self):
#         self.assertEqual(self.genre.name, "Western")
#
#     def test_has_api_id(self):
#         self.assertEqual(self.genre.api_id, 1)
#
#     def test_str(self):
#         expected = "Western"
#         actual = str(self.genre)
#
#         self.assertEqual(expected, actual)

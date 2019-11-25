from django.test import TestCase

from user.serializers import AuthorSerializer
from user.tests.helpers import create_user, create_university


class UserSerializersTests(TestCase):

    def setUp(self):
        self.user = create_user(first_name='Serializ')
        self.university = create_university()

    def test_author_serializer_succeeds_without_user_or_university(self):
        data = {
            'first_name': 'Ray',
            'last_name': 'Man',
        }
        serializer = AuthorSerializer(data=data)
        self.assertTrue(serializer.is_valid())

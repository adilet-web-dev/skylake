from django.test import TestCase
from rest_framework.test import APIClient
from users.factories import UserFactory


class GetPrivateUserIdAPITest(TestCase):
	def setUp(self) -> None:
		self.client = APIClient()

	def test_it_gets_private_id(self):
		user = UserFactory()
		response = self.client.post('/api/v1/users/get-private-id/', {
			"username": user.username,
			"password": user.password
		})

		self.assertEqual(response.data, user.private_id)

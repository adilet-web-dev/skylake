import json
import uuid

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from users.factories import UserFactory
from debates.factories import DebateFactory
from debates.models import Debate


class CreateDebateAPITest(TestCase):
	def setUp(self) -> None:
		self.client = APIClient()
		self.user = UserFactory()
		self.client.force_login(self.user)

		self.candidate_url = "/api/v1/debates/{}/add_candidates/"

	def test_it_creates_debate(self):

		payload = {
			"topic": "president",
			"description": "big debate for presidency",
			"stream": "https://www.youtube.com/watch?v=o0EgZ1SHtdg",
		}

		response = self.client.post("/api/v1/debates/", payload)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(Debate.objects.filter(topic="president").exists())

		payload = {"candidates": json.dumps(['Biden', 'Trump'])}

		response = self.client.post(self.candidate_url.format(response.data["id"]), payload)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Debate.objects.get(topic="president").candidates.count(), 2)

	def test_candidate_number_validation(self):
		debate = DebateFactory()
		response = self.client.post(self.candidate_url.format(debate.id), {
			"candidates": json.dumps(["Biden"])
		})

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

		response = self.client.post(self.candidate_url.format(debate.id), {
			"candidates": json.dumps(["Biden", "Harly", "Clinton", "Josh", "Bearn"])
		})

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



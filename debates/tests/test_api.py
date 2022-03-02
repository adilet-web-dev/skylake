import json
import uuid

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from users.factories import UserFactory
from debates.factories import DebateFactory, CandidateFactory
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


	def test_it_creates_debate_with_tags(self):
		payload = {
			"topic": "president",
			"stream": "https://www.youtube.com/watch?v=o0EgZ1SHtdg",
			"tags": json.dumps(["politics", "uefi"])
		}

		self.client.post("/api/v1/debates/", payload)
		debate = Debate.objects.get(topic=payload["topic"])
		self.assertEqual(debate.tags.count(), 2)

	def test_debate_creation_with_no_tags(self):
		payload = {
			"topic": "president",
			"stream": "https://www.youtube.com/watch?v=o0EgZ1SHtdg",
			"tags": "[]"
		}

		response = self.client.post("/api/v1/debates/", payload)
		self.assertEqual(response.status_code, 201)

		debate = Debate.objects.get(topic=payload["topic"])
		self.assertEqual(debate.tags.count(), 0)


class FilterDebateByTagListAPITest(TestCase):
	def setUp(self) -> None:
		self.client = APIClient()
		self.user = UserFactory()
		self.client.force_login(self.user)

	def test_it_gets_debate_by_tag(self):
		debate = DebateFactory()
		debate.tags.create(tag="test_tag")

		response = self.client.get("/api/v1/debates/filter&tag=test_tag")

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, debate.topic)


class SearchDebateListAPITest(TestCase):
	def setUp(self) -> None:
		self.client = APIClient()
		self.user = UserFactory()
		self.client.force_login(self.user)

	def test_it_finds_debate(self):
		debate = DebateFactory()

		response = self.client.get(f"/api/v1/debates/find={debate.topic[:3]}")

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, debate.topic)

	def test_finds_debate_by_candidate_name(self):
		debate = DebateFactory()
		candidate1 = CandidateFactory(debate=debate)
		candidate2 = CandidateFactory(debate=debate)

		response = self.client.get(f"/api/v1/debates/find={candidate1.name}")

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, debate.topic)

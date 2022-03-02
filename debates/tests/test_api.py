import json

from django.test import TestCase
from django.utils import timezone

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

		self.candidate_url = "/api/v1/debates/{}/add-candidates/"

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


class RecentDebatesListAPITest(TestCase):
	def setUp(self) -> None:
		self.client = APIClient()
		self.user = UserFactory()
		self.client.force_login(self.user)

	def test_it_returns_recent_debates(self):
		time1 = timezone.now() - timezone.timedelta(hours=1)
		time2 = timezone.now() - timezone.timedelta(hours=2)
		time3 = timezone.now() - timezone.timedelta(hours=3)

		debate1 = DebateFactory(created_at=time1)
		debate2 = DebateFactory(created_at=time2)
		debate3 = DebateFactory(created_at=time3)

		response = self.client.get("/api/v1/debates/recent/")

		self.assertEqual(response.status_code, 200)

		self.assertEqual(response.data[0]["topic"], debate1.topic)
		self.assertEqual(response.data[1]["topic"], debate2.topic)
		self.assertEqual(response.data[2]["topic"], debate3.topic)


class UserDebatesListAPITest(TestCase):
	def setUp(self) -> None:
		self.client = APIClient()
		self.user = UserFactory()
		self.client.force_login(self.user)

	def test_it_returns_users_debates(self):
		user = UserFactory()
		debates = DebateFactory.create_batch(3, owner=user)

		response = self.client.get(f"/api/v1/debates/user/{user.username}/")

		self.assertContains(response, debates[0].topic)
		self.assertContains(response, debates[1].topic)

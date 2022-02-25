import factory
from random import randint

from django.utils import timezone

from debates.models import Debate, Candidate
from users.factories import UserFactory


class DebateFactory(factory.django.DjangoModelFactory):
	topic = factory.Faker("name")
	created_at = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())
	ended_at = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())
	stream = factory.Faker("url")
	views = randint(0, 10000)
	owner = factory.SubFactory(UserFactory)

	class Meta:
		model = Debate


class CandidateFactory(factory.django.DjangoModelFactory):
	name = factory.Faker("name")
	debate = factory.SubFactory(DebateFactory)

	class Meta:
		model = Candidate

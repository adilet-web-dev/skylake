import factory
from random import randint

from django.utils import timezone

from debates.models import Debate


class DebateFactory(factory.django.DjangoModelFactory):
	topic = factory.Faker("name")
	created_at = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())
	ended_at = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())
	stream = factory.Faker("url")
	views = randint(0, 10000)

	class Meta:
		model = Debate

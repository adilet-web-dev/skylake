import factory
from random import randint

from debates.models import Debate


class DebateFactory(factory.django.DjangoModelFactory):
	topic = factory.Faker("name")
	created_at = factory.Faker("date_time")
	ended_at = factory.Faker("date_time")
	stream = factory.Faker("url")
	views = randint(0, 10000)

	class Meta:
		model = Debate

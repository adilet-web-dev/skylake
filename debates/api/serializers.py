from rest_framework.serializers import ModelSerializer
from django.utils import timezone

from debates.models import Debate, Candidate, Comment


class DebateSerializer(ModelSerializer):

	class Meta:
		model = Debate
		fields = [
			"topic",
			"created_at",
			"ended_at",
			"stream",
			"views",
			"id"
		]

	def create(self, validated_data):
		return Debate.objects.create(
			**validated_data,
			owner=self.context["request"].user,
			created_at=timezone.now()
		)


class CandidateSerializer(ModelSerializer):
	class Meta:
		model = Candidate
		fields = ["name", "votes", "voted_by_user"]


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
	def update(self, instance, validated_data):
		instance.topic= validated_data.get("topic", instance.topic)
		instance.created_at= validated_data.get("created_at", instance.created_at)
		instance.ended_at= validated_data.get("ended_at", instance.ended_at)
		instance.stream= validated_data.get("stream",instance.stream)
		instance.views= validated_data.get("views", instance.views)
		instance.save()
		return instance
	
class CandidateSerializer(ModelSerializer):
	class Meta:
		model = Candidate
		fields = ["name", "votes", "voted_by_user"]


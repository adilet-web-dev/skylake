from rest_framework.serializers import ModelSerializer

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


class CandidateSerializer(ModelSerializer):
	class Meta:
		model = Candidate
		fields = ["name", "votes", "voted_by_user"]


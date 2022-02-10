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
	debate = DebateSerializer()

	class Meta:
		model = Candidate
		fields = ["name", "votes", "debate"]


class CommentSerializer(ModelSerializer):
	debate = DebateSerializer()

	class Meta:
		model = Candidate
		fields = ["comment", "author", "debate"]

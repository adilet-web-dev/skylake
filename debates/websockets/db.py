from uuid import UUID
from voting.models import Vote
from channels.db import database_sync_to_async
from django.db.models import ObjectDoesNotExist

from debates.models import Debate, Candidate, Comment
from users.models import User


class AsyncDatabase:
	@database_sync_to_async
	def check_if_debate_exists(self, debate_id):
		return Debate.objects.filter(id=debate_id).exists()

	@database_sync_to_async
	def get_user_or_none(self, private_id: UUID):
		try:
			return User.objects.get(private_id=private_id)
		except ObjectDoesNotExist:
			return None

	@database_sync_to_async
	def add_vote_to_candidate(self, candidate, user, score, debate_id):
		debate = Debate.objects.get(id=debate_id)
		candidate = debate.candidates.get(name=candidate)

		Vote.objects.record_vote(candidate, user, score)

	@database_sync_to_async
	def get_total_votes(self, candidate):
		candidate = Candidate.objects.get(name=candidate)
		score = Vote.objects.get_score(candidate)["score"]
		return score

	@database_sync_to_async
	def create_comment(self, comment, debate_id, user):
		Comment.objects.create(
			debate_id=debate_id,
			comment=comment,
			author=user
		)

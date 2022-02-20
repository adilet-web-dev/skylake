from voting.models import Vote
from channels.db import database_sync_to_async

from debates.models import Debate, Candidate, Comment


class AsyncDatabase:
	@database_sync_to_async
	def check_if_debate_exists(self, debate_id):
		return Debate.objects.filter(id=debate_id).exists()

	@database_sync_to_async
	def is_authenticated(self, user):
		return user.is_authenticated

	@database_sync_to_async
	def add_vote_to_candidate(self, candidate, user, score, debate_id):
		debate = Debate.objects.get(id=debate_id)
		candidate = debate.candidates.get(name=candidate)

		vote = Vote.objects.get_for_user(candidate, user)
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

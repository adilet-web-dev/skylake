from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Debate(models.Model):
	topic = models.CharField(max_length=255)
	created_at = models.DateTimeField(null=True, blank=True)
	ended_at = models.DateTimeField(null=True, blank=True)
	stream = models.URLField(help_text="youtube live stream link")
	views = models.PositiveIntegerField(default=0)


class Candidate(models.Model):
	name = models.CharField(max_length=255)
	votes = models.IntegerField(default=0)
	debate = models.ForeignKey(Debate, on_delete=models.CASCADE, related_name="candidates")
	voted_by_user = models.BooleanField(default=False)


class Comment(models.Model):
	comment = models.CharField(max_length=300)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
	debate = models.ForeignKey(Debate, on_delete=models.CASCADE, related_name="comments")

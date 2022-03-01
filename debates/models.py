from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


User = get_user_model()


class TaggedItem(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.tag


class Debate(models.Model):
    topic = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    stream = models.URLField(help_text="youtube live stream link")
    views = models.PositiveIntegerField(default=0)
    owner = models.ForeignKey(User, related_name="debates", on_delete=models.PROTECT)
    tags = GenericRelation(TaggedItem, related_query_name="debate")

    def __str__(self):
        return f"{self.topic} - {self.owner}. {self.created_at}"


class Candidate(models.Model):
    name = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)
    debate = models.ForeignKey(Debate, on_delete=models.CASCADE, related_name="candidates")
    voted_by_user = models.BooleanField(default=False)


class Comment(models.Model):
    comment = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    debate = models.ForeignKey(Debate, on_delete=models.CASCADE, related_name="comments")

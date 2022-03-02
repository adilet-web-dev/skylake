import json

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Q

from voting.models import Vote

from debates.models import Debate, Candidate, TaggedItem
from users.models import User
from debates.api.serializers import DebateSerializer, CandidateSerializer


class DebateViewSet(ModelViewSet):
	queryset = Debate.objects.all()
	serializer_class = DebateSerializer

	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):

		data = self.request.data
		tags = data.get("tags")

		debate = serializer.save(
			topic=data.get("topic"),
			stream=data.get("stream"),
			owner=self.request.user,
			created_at=timezone.now()
		)

		if tags is not None:
			tags = json.loads(tags) if type(tags) == str else tags

			for tag in tags:
				debate.tags.create(tag=tag)

		debate.save()

	@action(methods=["GET"], detail=False)
	def recent(self, request):
		debates = Debate.objects.order_by("-created_at")
		return Response(
			data=self.serializer_class(debates, many=True).data,
			status=200
		)


class AddCandidatesAPI(APIView):
	@swagger_auto_schema(request_body=CandidateSerializer())
	def post(self, request, pk):
		candidates = request.data["candidates"]
		candidates = json.loads(candidates) if type(candidates) == str else candidates
		if len(candidates) < 2 or len(candidates) > 4:

			debate = Debate.objects.last()
			if debate is not None:
				if debate.candidates.count() == 0:
					debate.delete()

			return Response(
				data={"message": "number of candidates must be 2, 3 or 4"},
				status=status.HTTP_400_BAD_REQUEST
			)

		debate = get_object_or_404(Debate, pk=pk)

		for candidate in candidates:
			Candidate.objects.create(debate=debate, name=candidate)
		return Response(status=status.HTTP_201_CREATED)


class GetDebateCandidatesAPI(APIView):
	@swagger_auto_schema(responses={200: CandidateSerializer()})
	def get(self, request, pk):
		debate = get_object_or_404(Debate, pk=pk)
		candidates = []
		for candidate in debate.candidates.all():
			candidate.votes = Vote.objects.get_score(candidate)["score"]
			if Vote.objects.get_for_user(candidate, self.request.user) is not None:
				candidate.voted_by_user = True
			else:
				candidate.voted_by_user = False
			candidate.save()
			candidates.append(candidate)

		serializer = CandidateSerializer(candidates, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


class FilterDebateByTagListAPI(ListAPIView):
	serializer_class = DebateSerializer
	permission_classes = [IsAuthenticated]
	lookup_url_kwarg = "query"

	def get_queryset(self):
		query = self.kwargs.get(self.lookup_url_kwarg)
		tag = get_object_or_404(TaggedItem, tag=query)
		return tag.debates.all()


class SearchDebateListAPI(ListAPIView):
	serializer_class = DebateSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		query = self.kwargs.get("query")
		debates = Debate.objects.filter(
			Q(topic__icontains=query) | Q(candidates__name__icontains=query)
		)

		return debates


class UserDebateListAPI(ListAPIView):
	serializer_class = DebateSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		username = self.kwargs.get("username")
		user = get_object_or_404(User, username=username)
		return user.debates.all()

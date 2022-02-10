import json

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from debates.models import Debate, Candidate
from debates.api.serializers import DebateSerializer, CandidateSerializer


class DebateViewSet(ModelViewSet):
	queryset = Debate.objects.all()
	serializer_class = DebateSerializer

	@action(methods=["POST"], detail=True)
	def add_candidates(self, request, pk):
		candidates = request.data["candidates"]
		if len(candidates) < 2 or len(candidates) > 4:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		debate = self.get_object()

		for candidate in candidates:
			Candidate.objects.create(debate=debate, name=candidate)
		return Response(status=status.HTTP_201_CREATED)

	@action(methods=["GET"], detail=True)
	def get_candidates(self, request, pk):
		debate = self.get_object()
		serializer = CandidateSerializer(debate.candidates.all(), many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

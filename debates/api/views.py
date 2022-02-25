from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from voting.models import Vote

from debates.models import Debate, Candidate
from debates.api.serializers import DebateSerializer, CandidateSerializer, CandidateDebateSerilizer


class DebateViewSet(ModelViewSet):
	queryset = Debate.objects.all()
	serializer_class = DebateSerializer

	permission_classes = [IsAuthenticated]

	@action(methods=["POST"], detail=True)
	def add_candidates(self, request, pk):
		candidates = request.data["candidates"]
		if len(candidates) < 2 or len(candidates) > 4:

			debate = Debate.objects.last()
			if debate.candidates.count() == 0:
				debate.delete()

			return Response(
				data={"message": "number of candidates must be 2, 3 or 4"},
				status=status.HTTP_400_BAD_REQUEST
			)

		debate = self.get_object()

		for candidate in candidates:
			Candidate.objects.create(debate=debate, name=candidate)
		return Response(status=status.HTTP_201_CREATED)

	@action(methods=["GET"], detail=True)
	def get_candidates(self, request, pk):
		debate = self.get_object()
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

	@action(methods=["delete"], detail=True)
	def delete_debate(self,request, pk):
		debate= self.get_object()
		debate.delete()
		return Response(status=status.HTTP_200_OK)

	@action(methods=["PUT"], detail=True)
	def put_debate(self,request,pk):
		debate= self.get_object()
		serializer= DebateSerializer(debate,data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(data=serializer.data, status= status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class search_debate_view(APIView):
	permission_classes=[IsAuthenticated]
	def get(self,request, topic):
		debates= Debate.objects.filter(topic__icontains=topic)
		if debates.exists():
			serializer=DebateSerializer(debates, many=True)
			return Response(data=serializer.data, status=status.HTTP_200_OK)
		return Response(status=status.HTTP_204_NO_CONTENT)

class search_with_candidate_view(APIView):
	permission_classes=[IsAuthenticated]
	def get(self,request, candidate):
		candidates= Candidate.objects.filter(name__icontains=candidate)
		if candidates.exists():
			serializer= CandidateDebateSerilizer(candidates,many=True)
			data = [d["debate"] for d in serializer.data]
			return Response(data=data,status= status.HTTP_200_OK)
		return Response(status=status.HTTP_204_NO_CONTENT)

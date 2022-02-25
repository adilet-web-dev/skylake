from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import ObjectDoesNotExist

from users.models import User


class GetPrivateUserIdAPI(APIView):
	def post(self, request):
		data = request.data
		try:
			user = User.objects.get(name=data["username"])

			if user.password == data["password"]:
				return Response(data=user.private_id, status=status.HTTP_200_OK)
			else:
				return Response(status=status.HTTP_403_FORBIDDEN)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_403_FORBIDDEN)

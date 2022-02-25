from django.urls import path
from users.api.views import GetPrivateUserIdAPI


urlpatterns = [
	path('get-private-id/', GetPrivateUserIdAPI.as_view(), name="get_private_id")
]
from django.urls import path
from debates.api.views import (
    FilterDebateByTagListAPI,
    SearchDebateListAPI,
    AddCandidatesAPI,
    GetDebateCandidatesAPI,
    UserDebateListAPI
)


urlpatterns = [
    path("<int:pk>/add-candidates/", AddCandidatesAPI.as_view(), name="add_candidates"),
    path("<int:pk>/candidates/", GetDebateCandidatesAPI.as_view(), name="get_debate_candidates"),
    path("user/<str:username>/", UserDebateListAPI.as_view(), name="user_debates"),
    path("filter&tag=<str:query>", FilterDebateByTagListAPI.as_view(), name="filter_debate"),
    path("find=<str:query>", SearchDebateListAPI.as_view(), name="search_debate"),
]
from django.urls import path
from debates.api.views import FilterDebateByTagListAPI, SearchDebateListAPI


urlpatterns = [
    path("filter&tag=<str:query>", FilterDebateByTagListAPI.as_view(), name="filter_debate"),
    path("find=<str:query>", SearchDebateListAPI.as_view(), name="search_debate")
]
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView


urlpatterns = [
    path('users/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),

    path('', RedirectView.as_view(url=reverse_lazy("debate_list"))),
    path('debates/', include('debates.urls')),
    path('api/v1/', include('config.api_routers')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/debates/', include('debates.api_urls')),

    # about authentication endpoints read in
    # https://dj-rest-auth.readthedocs.io/en/latest/api_endpoints.html
    path('api/v1/auth/', include('dj_rest_auth.urls')),
    path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls'))
]

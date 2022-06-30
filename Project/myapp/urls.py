from django.urls import path
from .views import *

app_name="myapp"

urlpatterns=[
	path("",MyView.as_view(),name="Home"),
	path("playlist/",MyPlaylistView.as_view(),name="playlist"),
	path('login/',LoginView.as_view(),name="login"),
    path('signup/',SignupView.as_view(),name="signup"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('api/',addplaylist_api.as_view(),name="add"),
    path('api/remove/',removeplaylist_api.as_view(),name="remove"),
]
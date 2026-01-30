from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("feed/", views.feed, name="feed"),

    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

    path("t/<int:thread_id>/", views.thread_detail, name="thread_detail"),
    path("t/<int:thread_id>/like/", views.toggle_like, name="toggle_like"),

    path("u/<str:username>/", views.profile_view, name="profile"),
    path("u/<str:username>/follow/", views.toggle_follow, name="toggle_follow"),
    path("settings/profile/", views.edit_profile, name="edit_profile"),
]

from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("feed/", views.feed, name="feed"),
    path("post/new/", views.create_post, name="create_post"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("communities/", views.communities, name="communities"),
    path("messages/", views.inbox, name="inbox"),
]

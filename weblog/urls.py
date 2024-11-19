from django.urls import path

from .views import *

urlpatterns = [
	path("signup", signup, name="signup"),
	path("", index, name="home"),
	path("profile/<int:id>/", profile, name="profile"),
	path("edit_profile/<int:id>/", edit_profile, name="edit_profile"),
	path("new_blog/<int:id>/", new_blog, name="new_blog"),
	path('blog/<int:id>/', blog, name='blog'),
	path("sign-in", signin, name="sign-in"),
	path("create-profile/<int:id>/", create_profile, name="create-profile"),
	path("<str:action>/<str:other>/<int:id>/", like, name="like"),
	path("follow/<int:id>/", follow, name="follow"),
	path("comment/<int:id>/", new_comment, name="comment")
]
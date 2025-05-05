from django.urls import path
from . import views

urlpatterns = [
  path("register/", views.register, name="register"),
  path("login/", views.login, name="login"),
  path("profile/me/", views.get_user, name="get_user"),
  path("profile/<str:user_id>/", views.get_user_by_id, name="get_user"),
  path("update_profile/", views.update_user, name="update_profile"),
  path("delete_profile/", views.delete_user, name="delete_profile"),
]

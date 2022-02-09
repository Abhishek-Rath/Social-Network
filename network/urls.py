
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:user>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("follow/<str:user>/<str:curr_user>", views.follow, name="follow"),
    path("edit/<int:id>", views.edit, name="edit"),
    path('like/', views.like, name="like"),
    path("delete/<int:id>", views.delete, name="delete")
]

from django.contrib.auth import views as auth_views
from django.urls import path

from .forms import StyledAuthenticationForm
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="dashboard/login.html",
            authentication_form=StyledAuthenticationForm,
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("notes/", views.notes, name="notes"),
    path("notes/<int:pk>/", views.note_detail, name="note_detail"),
    path("notes/<int:pk>/delete/", views.note_delete, name="note_delete"),
    path("homework/", views.homework, name="homework"),
    path("homework/<int:pk>/toggle/", views.homework_toggle, name="homework_toggle"),
    path("homework/<int:pk>/delete/", views.homework_delete, name="homework_delete"),
    path("todo/", views.todo, name="todo"),
    path("todo/<int:pk>/toggle/", views.todo_toggle, name="todo_toggle"),
    path("todo/<int:pk>/delete/", views.todo_delete, name="todo_delete"),
    path("books/", views.books, name="books"),
    path("dictionary/", views.dictionary, name="dictionary"),
    path("wiki/", views.wiki, name="wiki"),
    path("youtube/", views.youtube, name="youtube"),
    path("conversion/", views.conversion, name="conversion"),
]

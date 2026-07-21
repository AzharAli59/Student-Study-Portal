from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from dashboard.forms import RegistrationForm
from dashboard.models import Homework, Todo


def home(request):
    return render(request, "dashboard/home.html")


def register(request):
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        auth_login(request, user)
        messages.success(request, "Your account has been created.")
        return redirect("profile")

    return render(request, "dashboard/register.html", {"form": form})


@login_required
def profile(request):
    todos = Todo.objects.filter(user=request.user)
    homeworks = Homework.objects.filter(user=request.user)
    return render(
        request,
        "dashboard/profile.html",
        {
            "todos": todos,
            "has_todos": todos.exists(),
            "homeworks": homeworks,
            "has_homeworks": homeworks.exists(),
        },
    )

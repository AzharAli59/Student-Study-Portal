from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from dashboard.forms import HomeworkForm, NoteForm, TodoForm
from dashboard.models import Homework, Note, Todo


@login_required
def notes(request):
    form = NoteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        note = form.save(commit=False)
        note.user = request.user
        note.save()
        messages.success(request, "Note created.")
        return redirect("notes")

    user_notes = Note.objects.filter(user=request.user)
    return render(
        request,
        "dashboard/notes.html",
        {"form": form, "notes": user_notes, "has_notes": user_notes.exists()},
    )


@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, "dashboard/note_detail.html", {"note": note})


@login_required
@require_POST
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.delete()
    messages.success(request, "Note deleted.")
    return redirect("notes")


@login_required
def homework(request):
    form = HomeworkForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        messages.success(request, "Homework created.")
        return redirect("homework")

    homeworks = Homework.objects.filter(user=request.user)
    return render(
        request,
        "dashboard/homework.html",
        {"form": form, "homeworks": homeworks, "has_homeworks": homeworks.exists()},
    )


@login_required
@require_POST
def homework_toggle(request, pk):
    item = get_object_or_404(Homework, pk=pk, user=request.user)
    item.is_completed = not item.is_completed
    item.save(update_fields=["is_completed", "updated_at"])
    return redirect("homework")


@login_required
@require_POST
def homework_delete(request, pk):
    item = get_object_or_404(Homework, pk=pk, user=request.user)
    item.delete()
    messages.success(request, "Homework deleted.")
    return redirect("homework")


@login_required
def todo(request):
    form = TodoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        messages.success(request, "Todo created.")
        return redirect("todo")

    todos = Todo.objects.filter(user=request.user)
    return render(
        request,
        "dashboard/todo.html",
        {"form": form, "todos": todos, "has_todos": todos.exists()},
    )


@login_required
@require_POST
def todo_toggle(request, pk):
    item = get_object_or_404(Todo, pk=pk, user=request.user)
    item.is_completed = not item.is_completed
    item.save(update_fields=["is_completed", "updated_at"])
    return redirect("todo")


@login_required
@require_POST
def todo_delete(request, pk):
    item = get_object_or_404(Todo, pk=pk, user=request.user)
    item.delete()
    messages.success(request, "Todo deleted.")
    return redirect("todo")

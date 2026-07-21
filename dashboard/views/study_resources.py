from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from dashboard.forms import SearchForm
from dashboard.services.study_resources import (
    StudyResourceError,
    lookup_dictionary_word,
    search_books,
    search_wikipedia,
    search_youtube,
)


@login_required
def books(request):
    form = SearchForm(request.POST or None)
    results = []

    if request.method == "POST" and form.is_valid():
        try:
            results = search_books(form.cleaned_data["text"])
        except StudyResourceError as exc:
            messages.error(request, str(exc))

    return render(request, "dashboard/books.html", {"form": form, "results": results})


@login_required
def dictionary(request):
    form = SearchForm(request.POST or None)
    result = None

    if request.method == "POST" and form.is_valid():
        try:
            result = lookup_dictionary_word(form.cleaned_data["text"])
        except StudyResourceError as exc:
            messages.error(request, str(exc))

    return render(request, "dashboard/dictionary.html", {"form": form, "result": result})


@login_required
def wiki(request):
    form = SearchForm(request.POST or None)
    result = None

    if request.method == "POST" and form.is_valid():
        try:
            result = search_wikipedia(form.cleaned_data["text"])
        except StudyResourceError as exc:
            messages.error(request, str(exc))

    return render(request, "dashboard/wiki.html", {"form": form, "result": result})


@login_required
def youtube(request):
    form = SearchForm(request.POST or None)
    results = []

    if request.method == "POST" and form.is_valid():
        try:
            results = search_youtube(form.cleaned_data["text"])
        except StudyResourceError as exc:
            messages.error(request, str(exc))

    return render(request, "dashboard/youtube.html", {"form": form, "results": results})

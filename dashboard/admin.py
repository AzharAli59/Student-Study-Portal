from django.contrib import admin

from .models import Homework, Note, Todo


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "title", "updated_at"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["title", "description", "user__username"]


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "subject", "title", "due_at", "is_completed"]
    list_filter = ["is_completed", "due_at", "created_at"]
    search_fields = ["subject", "title", "description", "user__username"]


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "title", "is_completed", "updated_at"]
    list_filter = ["is_completed", "created_at", "updated_at"]
    search_fields = ["title", "user__username"]

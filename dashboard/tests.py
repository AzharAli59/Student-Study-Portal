from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Homework, Note, Todo
from .services.conversion import convert_measurement


class DashboardAuthTests(TestCase):
    def test_auth_pages_render(self):
        for route_name in ["login", "register"]:
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, 200)

    def test_profile_requires_login(self):
        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_registration_creates_and_logs_in_user(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "portfolio_user",
                "email": "user@example.com",
                "password1": "StrongPassword123!",
                "password2": "StrongPassword123!",
            },
        )

        self.assertRedirects(response, reverse("profile"))
        self.assertTrue(User.objects.filter(username="portfolio_user").exists())


class PageRenderTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="azhar", password="pass12345")
        self.client.force_login(self.user)

    def test_main_pages_render(self):
        route_names = [
            "home",
            "profile",
            "notes",
            "homework",
            "todo",
            "books",
            "dictionary",
            "wiki",
            "youtube",
            "conversion",
        ]

        for route_name in route_names:
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, 200)


class NoteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="azhar", password="pass12345")
        self.other_user = User.objects.create_user(username="other", password="pass12345")
        self.client.force_login(self.user)

    def test_create_note_assigns_logged_in_user(self):
        response = self.client.post(
            reverse("notes"),
            {"title": "Django", "description": "Study forms and views."},
        )

        self.assertRedirects(response, reverse("notes"))
        note = Note.objects.get(title="Django")
        self.assertEqual(note.user, self.user)

    def test_user_cannot_view_another_users_note(self):
        note = Note.objects.create(
            user=self.other_user,
            title="Private",
            description="Not visible",
        )

        response = self.client.get(reverse("note_detail", args=[note.id]))

        self.assertEqual(response.status_code, 404)

    def test_delete_note_requires_owner_and_post(self):
        note = Note.objects.create(
            user=self.other_user,
            title="Private",
            description="Not deletable",
        )

        get_response = self.client.get(reverse("note_delete", args=[note.id]))
        post_response = self.client.post(reverse("note_delete", args=[note.id]))

        self.assertEqual(get_response.status_code, 405)
        self.assertEqual(post_response.status_code, 404)
        self.assertTrue(Note.objects.filter(pk=note.pk).exists())


class HomeworkAndTodoTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="azhar", password="pass12345")
        self.client.force_login(self.user)

    def test_create_homework_assigns_logged_in_user(self):
        response = self.client.post(
            reverse("homework"),
            {
                "subject": "Math",
                "title": "Algebra",
                "description": "Chapter 2",
                "due_at": "2026-07-22T10:30",
            },
        )

        self.assertRedirects(response, reverse("homework"))
        homework = Homework.objects.get(title="Algebra")
        self.assertEqual(homework.user, self.user)

    def test_toggle_todo_requires_post(self):
        todo = Todo.objects.create(user=self.user, title="Read")

        get_response = self.client.get(reverse("todo_toggle", args=[todo.id]))
        post_response = self.client.post(reverse("todo_toggle", args=[todo.id]))

        todo.refresh_from_db()
        self.assertEqual(get_response.status_code, 405)
        self.assertRedirects(post_response, reverse("todo"))
        self.assertTrue(todo.is_completed)


class ConversionTests(TestCase):
    def test_convert_measurement(self):
        self.assertEqual(convert_measurement(2, "yard", "foot"), "2 yard = 6 foot")
        self.assertEqual(convert_measurement(1, "kilogram", "pound"), "1 kilogram = 2.20462 pound")

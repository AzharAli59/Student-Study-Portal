# Student Study Portal

Student Study Portal is a Django web application for students who want one place to manage study work and quickly search learning resources.

The project is intentionally simple and portfolio-friendly: it uses Django server-rendered pages, SQLite for local development, Bootstrap for styling, and a small set of external APIs for resource search.

## What the app does

Authenticated users can:

- Create, view, and delete personal notes
- Create, track, complete, and delete homework
- Create, complete, and delete todos
- View a profile dashboard summarizing todos and homework
- Search books using Google Books
- Look up word meanings using a dictionary API
- Search Wikipedia summaries
- Search YouTube videos
- Convert supported length and mass units

## Tech stack

- Python 3.12+
- Django 5.2
- SQLite for local development
- Bootstrap 4
- `uv` for dependency and virtual environment management

## Directory structure

```text
Student-Study-Portal/
├── manage.py
├── pyproject.toml
├── uv.lock
├── README.md
├── .gitignore
├── study_portal/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── dashboard/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    ├── migrations/
    │   ├── __init__.py
    │   └── 0001_initial.py
    ├── services/
    │   ├── __init__.py
    │   ├── conversion.py
    │   └── study_resources.py
    ├── static/
    │   ├── css/
    │   │   └── portal.css
    │   └── images/
    ├── templates/
    │   └── dashboard/
    │       ├── base.html
    │       ├── home.html
    │       ├── profile.html
    │       ├── login.html
    │       ├── register.html
    │       ├── notes.html
    │       ├── note_detail.html
    │       ├── homework.html
    │       ├── todo.html
    │       ├── books.html
    │       ├── dictionary.html
    │       ├── wiki.html
    │       ├── youtube.html
    │       └── conversion.html
    └── views/
        ├── __init__.py
        ├── accounts.py
        ├── study_tasks.py
        ├── study_resources.py
        └── unit_conversion.py
```

## How the code is organized

### `study_portal/`

This is the Django project configuration package.

- `settings.py`: global Django settings, installed apps, database, templates, static files, login redirects, and environment variable support
- `urls.py`: project-level URL routing; it includes the `dashboard` app routes
- `asgi.py` and `wsgi.py`: deployment entry points

### `dashboard/`

This is the main application. It contains all user-facing study portal behavior.

- `models.py`: database models for `Note`, `Homework`, and `Todo`
- `forms.py`: Django forms used by templates and views
- `urls.py`: app-level URL routes
- `admin.py`: Django admin configuration
- `tests.py`: regression tests for authentication, ownership, page rendering, and conversions
- `templates/dashboard/`: HTML templates
- `static/css/portal.css`: app styling
- `static/images/`: home-page feature images

### `dashboard/views/`

Views are split by behavior instead of keeping everything in one large file.

- `accounts.py`: home page, registration, and profile dashboard
- `study_tasks.py`: notes, homework, and todo CRUD/status behavior
- `study_resources.py`: book, dictionary, Wikipedia, and YouTube search pages
- `unit_conversion.py`: conversion page behavior
- `__init__.py`: exports the view functions so `dashboard/urls.py` can import them cleanly

### `dashboard/services/`

Service files contain reusable business/API logic.

- `conversion.py`: unit conversion logic
- `study_resources.py`: external API integrations for books, dictionary, Wikipedia, and YouTube

This keeps views focused on HTTP request/response handling.

## Data model

The app has three main models.

### `Note`

Stores personal notes for a logged-in user.

Important fields:

- `user`: owner of the note
- `title`: note title
- `description`: full note content
- `created_at`, `updated_at`: timestamps

### `Homework`

Stores homework or assignment tasks.

Important fields:

- `user`: owner of the homework item
- `subject`: subject name
- `title`: homework title
- `description`: optional details
- `due_at`: optional due date and time
- `is_completed`: completion status
- `created_at`, `updated_at`: timestamps

### `Todo`

Stores simple personal todo items.

Important fields:

- `user`: owner of the todo
- `title`: todo text
- `is_completed`: completion status
- `created_at`, `updated_at`: timestamps

## Security behavior

The app includes the important basics for a multi-user Django app:

- Notes, homework, and todos are filtered by the logged-in user
- Detail/update/delete actions verify object ownership
- Create forms do not expose the `user` field
- The server assigns `request.user` when saving user-owned objects
- Delete and toggle actions require POST requests
- CSRF protection is used in forms
- Login is required for all personal dashboard and study tool pages

## External services

The app uses public/external services:

- Google Books API for book search
- Dictionary API at `dictionaryapi.dev`
- Wikipedia through the `wikipedia` Python package
- YouTube search through `youtube-search-python`

External calls use request timeouts where supported and show user-friendly error messages when a provider fails.

## Local setup

Install `uv` first if it is not already installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install project dependencies:

```bash
uv sync
```

Create the local database:

```bash
uv run python manage.py migrate
```

Create an admin user:

```bash
uv run python manage.py createsuperuser
```

Run the development server:

```bash
uv run python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Useful commands

Run Django system checks:

```bash
uv run python manage.py check
```

Run tests:

```bash
uv run python manage.py test dashboard
```

Create migrations after model changes:

```bash
uv run python manage.py makemigrations
```

Apply migrations:

```bash
uv run python manage.py migrate
```

Open Django shell:

```bash
uv run python manage.py shell
```

## Environment variables

The project runs locally without extra environment variables. For deployment, configure:

```text
DJANGO_SECRET_KEY=replace-with-a-secure-secret
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_TIME_ZONE=UTC
```

## GitHub notes

The repository intentionally ignores generated/runtime files:

- `.venv/`
- `__pycache__/`
- `db.sqlite3`
- `staticfiles/`
- `.env`
- IDE folders like `.idea/` and `.vscode/`

After cloning, a new developer should run:

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

## Current validation status

The project has been validated with:

```bash
uv run python manage.py check
uv run python manage.py test dashboard
uv run python manage.py makemigrations --check --dry-run
```

Expected result:

```text
System check identified no issues
All tests pass
No model migration changes detected
```

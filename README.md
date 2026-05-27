# Blog API

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![Django](https://img.shields.io/badge/django-4.2-green)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/djangorestframework-3.14-red)](https://www.django-rest-framework.org/)

A feature-rich Blog REST API built with Django REST Framework, featuring full CRUD, filtering, pagination, and auto-generated documentation.

## Features

- Full CRUD for Posts, Comments, Categories, Tags, Users
- Post filtering by status, category, author, featured status
- Search by title, content, excerpt
- Pagination (10 per page)
- Comment moderation (admin approval)
- Featured posts and related posts
- View tracking on posts
- Auto-generated Swagger UI and ReDoc documentation
- CORS enabled

## API Documentation

- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

## Setup

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Tech Stack

- Django 4.2
- Django REST Framework 3.14
- django-filter
- django-cors-headers
- drf-yasg (Swagger/ReDoc)
- SQLite

## License

MIT

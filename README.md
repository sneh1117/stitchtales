# StitchTales 🧶

A full-featured blogging platform built for the crochet and knitting community. StitchTales allows creators to share tutorials, patterns, and stories — with a clean writing experience, image uploads via Supabase, and a REST API for extensibility.

**Live:** [stitchtales.up.railway.app](https://stitchtales.up.railway.app)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [Deployment](#deployment)
- [Roadmap](#roadmap)

---

## Overview

StitchTales is a Django-based blog application designed around community-driven content. Authors can register, manage their profiles, write and publish posts with cover images, and interact with other creators through comments and likes. The platform is deployed on Railway with media files stored on Supabase Storage.

---

## Features

### Blog CRUD
- Create, edit, and delete posts with a rich text editor
- Draft and publish workflow — posts stay private until you're ready
- Auto-generated slugs, reading time estimates, and excerpts
- Category and tag organization
- View count tracking per post
- SEO fields — meta description and keywords per post

### User Authentication & Profiles
- Register and log in with username/password
- Personal profile pages with bio, avatar, and social links (Instagram, Pinterest)
- Author detail pages showing all published posts
- Login-required protection on all write actions

### Supabase Image Storage
- Cover images and avatars uploaded directly to Supabase Storage
- Custom Django storage backend — no dependency on AWS or Cloudinary
- Public CDN URLs for fast image delivery
- Organized into `covers/` and `avatars/` folders within the bucket

### REST API
- Built with Django REST Framework
- Token and session authentication
- Paginated post listings
- Read-only access for unauthenticated users
- Full CRUD for authenticated authors

### Additional
- HTMX-powered like button (no page reload)
- Comment system with moderation (approve before display)
- Search across post titles and content
- Sitemap (`/sitemap.xml`) and `robots.txt` for SEO
- Custom 404 and 500 error pages
- Whitenoise for static file serving in production

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.2, Django REST Framework |
| Database | PostgreSQL (Railway) / SQLite (local) |
| Media Storage | Supabase Storage |
| Static Files | Whitenoise |
| Deployment | Railway |
| Auth | Django built-in auth + DRF Token Auth |
| Frontend | Django Templates, HTMX |

---

## Project Structure

```
stitchtales/
├── blog/
│   ├── models.py           # Post, Category, Tag, Comment, Like, UserProfile
│   ├── views.py            # All view logic
│   ├── forms.py            # RegisterForm, PostForm, ProfileForm, CommentForm
│   ├── storage_backends.py # Custom Supabase Storage backend
│   ├── urls.py
│   ├── serializers.py      # DRF serializers
│   └── templates/
│       ├── blog/
│       └── auth/
├── stitchtales/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── staticfiles/
├── requirements.txt
└── manage.py
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- A Supabase account with a storage bucket created
- PostgreSQL (for production) or SQLite (for local dev)

### Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/sneh1117/stitchtales.git
cd stitchtales

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file (see Environment Variables section)

# 5. Run migrations
python manage.py migrate

# 6. Create a superuser
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver
```

---

## Environment Variables

Create a `.env` file in the project root with the following:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database (leave as default for SQLite locally)
DATABASE_URL=sqlite:///db.sqlite3

# Supabase Storage
USE_SUPABASE=True
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
SUPABASE_BUCKET=media

# CSRF (production only)
CSRF_TRUSTED_ORIGINS=https://yourdomain.up.railway.app
```

> **Important:** Use the **service role key** from Supabase (Settings → API), not the anon key. The service role key is required for server-side file uploads.

---

## API Reference

Base URL: `https://stitchtales.up.railway.app/api/`

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| GET | `/api/posts/` | No | List all published posts |
| GET | `/api/posts/<slug>/` | No | Retrieve a single post |
| POST | `/api/posts/` | Yes | Create a new post |
| PUT | `/api/posts/<slug>/` | Yes | Update a post |
| DELETE | `/api/posts/<slug>/` | Yes | Delete a post |
| POST | `/api/auth/token/` | No | Obtain auth token |

### Authentication

```bash
# Get a token
curl -X POST https://stitchtales.up.railway.app/api/auth/token/ \
  -d "username=youruser&password=yourpassword"

# Use the token
curl https://stitchtales.up.railway.app/api/posts/ \
  -H "Authorization: Token your-token-here"
```

---

## Deployment

StitchTales is deployed on [Railway](https://railway.app).

### Steps to deploy your own instance

1. Push your code to GitHub
2. Create a new project on Railway and connect your repository
3. Add a PostgreSQL plugin inside Railway
4. Set all environment variables in Railway's variable settings
5. Railway will auto-detect the Django app and deploy using `gunicorn`

### Required Railway Environment Variables

```
SECRET_KEY
DEBUG=False
ALLOWED_HOSTS=yourapp.up.railway.app
DATABASE_URL          # auto-set by Railway PostgreSQL plugin
USE_SUPABASE=True
SUPABASE_URL
SUPABASE_KEY
SUPABASE_BUCKET=media
CSRF_TRUSTED_ORIGINS=https://yourapp.up.railway.app
```

---

## Roadmap

- [ ] Rich text editor (TipTap or Quill) for post content
- [ ] Email notifications for comments
- [ ] Newsletter subscription
- [ ] Pattern file uploads (PDF support)
- [ ] Social login (Google, GitHub)
- [ ] Dark mode toggle

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

*Built with 🧶 by [Sneha](https://github.com/sneh1117)*

# StitchTales 🧶

![CI](https://github.com/sneh1117/stitchtales/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.2-green?logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Railway-blue?logo=postgresql)
![Deployed](https://img.shields.io/badge/Deployed-Railway-blueviolet?logo=railway)
![License](https://img.shields.io/badge/License-MIT-yellow)

A full-featured blogging platform built for the crochet and knitting community. StitchTales allows creators to share tutorials, patterns, and stories — with a clean writing experience, image uploads via Supabase, and a REST API for extensibility.

**Live Demo:** [stitchtales.up.railway.app](https://stitchtales.up.railway.app)

---

## Table of Contents

- [Overview](#overview)
- [Key Technical Highlights](#key-technical-highlights)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture Decisions](#architecture-decisions)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [Deployment](#deployment)
- [Roadmap](#roadmap)

---

## Overview

StitchTales is a Django-based blog platform designed around community-driven content. Authors can register, manage profiles, write and publish posts with cover images, and interact through comments and likes. The platform is deployed on Railway with media files stored on Supabase Storage.

This project was built end-to-end as a solo project — from database schema design to production deployment — covering the full Django web development stack including custom storage backends, REST API design, SEO optimisation, and visitor analytics.

---

## Key Technical Highlights

These are the more interesting engineering decisions made during development:

- **Custom Supabase Storage Backend** — wrote a custom Django `Storage` class to integrate Supabase as a media file host, replacing the need for AWS S3 or Cloudinary. Handles file upload, URL generation, and deletion through the Supabase REST API.

- **Visitor Analytics from Scratch** — built a lightweight analytics system using a `Visitor` model and middleware. Tracks page views, unique IPs, referrer URLs, and geographic data — without any third-party analytics service. Superuser-only dashboard displays top pages, countries, and referrers.

- **View Count Integrity** — post view counts only increment for visitors who are not the post author, preventing authors from inflating their own stats.

- **HTMX Like Button** — the like/unlike interaction uses HTMX for a seamless in-place UI update with no full page reload, and no JavaScript framework required.

- **SEO Infrastructure** — every post has meta description, keywords, Open Graph tags, and Twitter Card tags. A dynamic XML sitemap (`/sitemap.xml`) and `robots.txt` are served automatically.

- **Rich Text with Quill** — the post editor uses Quill.js (CDN, no backend dependency) with the content stored as HTML and rendered safely in templates.

- **Paginated Search with Filters** — search results can be filtered by category, tag, and sorted by newest, oldest, most viewed, or most liked — all in a single query using Django ORM with `.distinct()` to prevent duplicates from M2M joins.

---

## Features

### Blog
- Create, edit, and delete posts with a Quill rich text editor
- Draft and publish workflow
- Auto-generated slugs, reading time estimates, and excerpts
- Multiple cover image uploads per post (up to 3), displayed as a Bootstrap carousel
- Category and tag organisation with dedicated listing pages
- View count tracking (excludes author's own views)
- Related posts by category

### User Authentication & Profiles
- Register and log in with username/password
- Personal profile pages with bio, avatar, and social links (Instagram, Pinterest)
- Author detail pages showing all published posts
- Login-required protection on all write actions

### Search & Discovery
- Full-text search across post titles and content
- Filter by category and tag
- Sort by newest, oldest, most viewed, or most liked
- Pagination across all listing pages (home, search, category, tag)

### Visitor Analytics (Superuser)
- Total visits, unique visitors, and visits today
- Top pages by traffic
- Top referrer URLs
- Top countries (via IP geolocation)
- All tracked without third-party services

### REST API
- Built with Django REST Framework
- Token and session authentication
- Paginated post listings
- Read-only for unauthenticated users, full CRUD for authenticated authors

### Additional
- HTMX-powered like button (no page reload)
- Comment system with moderation (approve before display)
- XML sitemap and `robots.txt`
- Open Graph and Twitter Card meta tags per post
- Custom 404 and 500 error pages
- Whitenoise for static file serving in production

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.2, Django REST Framework |
| Database | PostgreSQL (Railway) / SQLite (local) |
| Media Storage | Supabase Storage (custom backend) |
| Static Files | Whitenoise |
| Frontend | Django Templates, HTMX, Quill.js |
| Deployment | Railway |
| Auth | Django built-in auth + DRF Token Auth |
| CI | GitHub Actions |

---

## Architecture Decisions

### Why Supabase instead of S3?
S3 requires AWS account setup, IAM roles, and bucket policies. Supabase Storage offers a simpler REST API with a generous free tier, making it a better fit for an indie project. A custom Django `Storage` subclass keeps the integration clean — the rest of the app doesn't know or care where files go.

### Why HTMX instead of React for likes?
The like button is the only truly interactive element. Adding a full JS framework for one button would be over-engineering. HTMX handles the partial HTML swap in ~5 lines of template markup, keeping the stack simple and the page fast.

### Why build analytics instead of using Google Analytics?
GA adds cookie consent requirements, GDPR complexity, and sends user data to a third party. A simple `Visitor` model in Postgres gives the same core insights (page views, referrers, geography) with full data ownership and no compliance overhead.

---

## Project Structure

```
stitchtales/
├── blog/
│   ├── models.py               # Post, Category, Tag, Comment, Like, UserProfile, Visitor
│   ├── views.py                # All view logic including analytics aggregation
│   ├── forms.py                # RegisterForm, PostForm, ProfileForm, CommentForm
│   ├── storage_backends.py     # Custom Supabase Storage backend
│   ├── middleware.py           # Visitor tracking middleware
│   ├── urls.py
│   ├── serializers.py          # DRF serializers
│   └── templates/
│       ├── blog/               # home, post_detail, dashboard, search, etc.
│       ├── auth/               # login, register, profile, author_detail
│       └── partials/           # like_button, pagination
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

Create a `.env` file in the project root:

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

> **Note:** Use the **service role key** from Supabase (Settings → API), not the anon key. The service role key is required for server-side file uploads.

---

## API Reference

Base URL: `https://stitchtales.up.railway.app/api/`

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| GET | `/api/posts/` | No | List all published posts (paginated) |
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

StitchTales is deployed on [Railway](https://railway.app) with zero-downtime deploys triggered automatically on every push to `main`.

### Steps to deploy your own instance

1. Push your code to GitHub
2. Create a new project on Railway and connect your repository
3. Add a PostgreSQL plugin inside Railway
4. Set all environment variables in Railway's variable settings
5. Railway auto-detects the Django app and deploys using `gunicorn`

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

- [x] Rich text editor (Quill) for post content
- [x] Search with category, tag, and sort filters
- [x] Pagination across all listing pages
- [x] Multiple cover images per post with carousel
- [x] Visitor analytics dashboard
- [ ] Email notifications for comments
- [ ] Comment threading (nested replies)
- [ ] Bookmarks / saved posts
- [ ] Share buttons (WhatsApp, copy link)
- [ ] Newsletter subscription
- [ ] Pattern file uploads (PDF support)
- [ ] Social login (Google, GitHub)

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

*Built with 🧶 by [Sneha](https://github.com/sneh1117)*

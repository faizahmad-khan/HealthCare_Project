# HealthCare Portal (Django)

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2%2B-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20PostgreSQL-336791)](#database-and-migrations)
[![Deployment](https://img.shields.io/badge/Deploy-Vercel-black?logo=vercel)](#deployment-vercel)

A full-stack healthcare management web application built with Django.

This project provides a complete portal to manage:
- patient records and vitals
- doctor profiles and specializations
- appointments and prescriptions
- pharmacy inventory and dispensing
- user authentication and profile management

It is designed as a server-rendered web app (Django templates), with local SQLite support for development and PostgreSQL-ready configuration for production deployment (including Vercel).

## Quick Links

- Live demo: Add your deployed URL here (for example: `https://your-project.vercel.app`)
- Deployment guide: `DEPLOYMENT.md`
- Main settings: `healthcare_dashboard/settings.py`
- Vercel entrypoint: `api/asgi.py`

## Table of Contents

- [Project Highlights](#project-highlights)
- [Tech Stack](#tech-stack)
- [Core Modules](#core-modules)
- [Project Structure](#project-structure)
- [How the App Works](#how-the-app-works)
- [Local Setup](#local-setup)
- [Environment Variables](#environment-variables)
- [Database and Migrations](#database-and-migrations)
- [Static and Media Files](#static-and-media-files)
- [Deployment (Vercel)](#deployment-vercel)
- [Common Management Commands](#common-management-commands)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)

## Project Highlights

- Authentication system (register, login, logout, profile)
- Dashboard with key healthcare metrics
- Patient lifecycle management:
  - create, update, delete
  - medical records
  - vital signs tracking (includes BMI calculation)
- Doctor lifecycle management:
  - create, update, soft-deactivate
  - specialization support
- Appointment management:
  - scheduling and filtering
  - status updates
  - today view
  - prescription creation
- Pharmacy management:
  - medicine catalog with categories
  - low-stock and expiry awareness
  - dispensing workflow with stock deduction
  - stock movement records
- Production-ready settings:
  - environment-based configuration
  - WhiteNoise static serving
  - PostgreSQL via DATABASE_URL
  - Vercel ASGI adapter through Mangum

## Screenshots

Add screenshots to a `screenshots/` folder and update these image paths.

![Home Page](screenshots/home-page.png)
![Dashboard](screenshots/dashboard.png)
![Patient Detail](screenshots/patient-detail.png)
![Appointment List](screenshots/appointment-list.png)
![Pharmacy Dashboard](screenshots/pharmacy-dashboard.png)

## Tech Stack

- Backend: Django 5.2+
- Database:
  - Development: SQLite (`db.sqlite3`)
  - Production: PostgreSQL (via `dj-database-url`)
- Frontend: Django Templates + Bootstrap
- Static files: WhiteNoise
- Image/file handling: Pillow
- Serverless adapter: Mangum
- Deployment target: Vercel (Python runtime 3.11)

Dependencies are listed in `requirements.txt`.

## Core Modules

### 1) Accounts (`healthcare_dashboard/accounts`)

Handles:
- user registration and login/logout
- profile management (`UserProfile`)
- app home page and dashboard

### 2) Patients (`healthcare_dashboard/patients`)

Handles:
- patient demographics and contact details
- emergency and insurance details
- medical records (`MedicalRecord`)
- vitals (`VitalRecord`) with computed BMI

### 3) Doctors (`healthcare_dashboard/doctors`)

Handles:
- doctor directory
- specializations (`Specialization`)
- scheduling metadata (days/time fields)
- soft deactivation using `is_active`

### 4) Appointments (`healthcare_dashboard/appointments`)

Handles:
- appointment booking and updates
- appointment status workflow
- "today's appointments" view
- one-to-one prescription per appointment
- multiple prescription items

### 5) Pharmacy (`healthcare_dashboard/pharmacy`)

Handles:
- medicine categories and medicine catalog
- stock levels and reorder thresholds
- dispensing and automatic stock deduction
- stock movement history and adjustments
- pharmacy dashboard metrics

## Project Structure

```
HealthCare_Project/
├── manage.py
├── requirements.txt
├── DEPLOYMENT.md
├── vercel.json
├── build_files.sh
├── db.sqlite3
├── api/
│   └── asgi.py                # Vercel entrypoint (Mangum handler)
├── healthcare_dashboard/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── accounts/
│   ├── patients/
│   ├── doctors/
│   ├── appointments/
│   ├── pharmacy/
│   ├── templates/
│   └── statics/
└── env/                        # local virtual environment (not for production)
```

## How the App Works

Main URL routing in `healthcare_dashboard/urls.py`:
- `/` -> accounts/home/auth/dashboard routes
- `/patients/` -> patient management
- `/doctors/` -> doctor management
- `/appointments/` -> appointment and prescription flows
- `/pharmacy/` -> inventory and dispensing
- `/admin/` -> Django admin

Authentication:
- Most management views use Django's `login_required` decorator.
- Login URL is configured as `/accounts/login/`.

Dashboard metrics:
- Counts of patients, doctors, appointments, medicines.
- Recent appointments and patients are shown on the dashboard.

## Local Setup

### Prerequisites

- Python 3.11+
- pip
- macOS/Linux terminal (or equivalent shell on Windows)

### 1) Clone and enter the project

```bash
git clone <your-repo-url>
cd HealthCare_Project
```

### 2) Create and activate virtual environment

```bash
python3 -m venv env
source env/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Apply migrations

```bash
python manage.py migrate
```

### 5) Create admin user (optional but recommended)

```bash
python manage.py createsuperuser
```

### 6) Run development server

```bash
python manage.py runserver
```

Open:
- Home page: `http://127.0.0.1:8000/`
- Admin panel: `http://127.0.0.1:8000/admin/`

## Environment Variables

The project reads configuration from environment variables in `healthcare_dashboard/settings.py`.

| Variable | Purpose | Example |
|---|---|---|
| `DJANGO_SECRET_KEY` | Secret key for Django | `a-long-random-secret` |
| `DJANGO_DEBUG` | Debug toggle (`True/False`) | `False` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed hosts | `127.0.0.1,localhost,.vercel.app` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Comma-separated HTTPS origins | `https://your-app.vercel.app` |
| `DATABASE_URL` | PostgreSQL connection string (production) | `postgresql://user:pass@host:5432/dbname` |
| `RUN_MIGRATIONS` | Run migrate during build script (`1` to enable) | `1` |
| `VERCEL` | Added by platform; used to append Vercel host/origin | `1` |

Behavior summary:
- If `DATABASE_URL` is not set, SQLite is used.
- If `DATABASE_URL` is set, PostgreSQL config is parsed automatically.
- In non-debug mode, secure cookies and proxy SSL headers are enabled.

## Database and Migrations

Local development:
- Uses SQLite by default (`db.sqlite3`).

Production:
- Use PostgreSQL and set `DATABASE_URL`.

Run migrations manually:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Static and Media Files

Static files:
- `STATIC_URL = /static/`
- `STATICFILES_DIRS = healthcare_dashboard/statics`
- `STATIC_ROOT = staticfiles`
- `collectstatic` is required for production
- WhiteNoise serves static files

Media files:
- `MEDIA_URL = /media/`
- `MEDIA_ROOT = media`
- In development, media is served when `DEBUG=True`

Important production note:
- Vercel's serverless filesystem is ephemeral, so user-uploaded media should be moved to persistent storage (for example S3, Cloudinary, or Supabase Storage).

## Deployment (Vercel)

This repository already includes deployment files:
- `vercel.json`
- `build_files.sh`
- `api/asgi.py` (Mangum handler)

### Recommended deployment flow

1. Push code to GitHub.
2. Import the repository into Vercel.
3. Add environment variables:
   - `DJANGO_SECRET_KEY`
   - `DJANGO_DEBUG=False`
   - `DJANGO_ALLOWED_HOSTS`
   - `DJANGO_CSRF_TRUSTED_ORIGINS`
   - `DATABASE_URL`
   - `RUN_MIGRATIONS=1` (first deploy)
4. Deploy.
5. Verify app, admin route, and static files.
6. Create superuser against production DB.
7. Set `RUN_MIGRATIONS=0` after initial migration run.

For full details, see `DEPLOYMENT.md`.

## Common Management Commands

```bash
# Run dev server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run tests
python manage.py test
```

## Troubleshooting

### DisallowedHost

Set `DJANGO_ALLOWED_HOSTS` correctly, including `.vercel.app` for Vercel deployments.

### CSRF failures in production

Set `DJANGO_CSRF_TRUSTED_ORIGINS` with full HTTPS origins.

### Static files not loading

- Make sure `collectstatic` runs successfully.
- Confirm `STATIC_ROOT=staticfiles`.
- Verify Vercel build logs.

### Database errors in production

- Validate `DATABASE_URL` format and credentials.
- Ensure your PostgreSQL provider allows remote connections.
- Ensure SSL is enabled where required.

## Future Improvements

- Role-based access control and permission matrix per module
- API layer (Django REST Framework) for mobile/client integrations
- Background jobs and notifications (appointments, refill reminders)
- Audit logs for sensitive healthcare actions
- Persistent cloud storage integration for user uploads
- Expanded automated test coverage (unit + integration)

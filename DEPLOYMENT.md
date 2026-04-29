# Django Deployment Guide (Vercel)

This project is already configured for Vercel with:
- `vercel.json`
- `build_files.sh`
- `requirements.txt`
- environment-based Django settings

Use this guide to deploy safely to production.

## 1. Prerequisites

- GitHub repository with this code pushed
- Vercel account
- PostgreSQL database (Neon, Supabase, Railway, Render, etc.)

Note: SQLite is not suitable for production on Vercel.

## 2. Production Architecture

- Django app runs as a Vercel Python serverless function via `healthcare_dashboard/wsgi.py`
- Static files are collected with `build_files.sh`
- Static files are served from `staticfiles`
- Database connection comes from `DATABASE_URL`

## 3. Create a PostgreSQL Database

You can use Neon or Supabase.

### Option A: Neon (recommended)

1. Create a new Neon project and database.
2. Copy the connection string.
3. Ensure SSL is enabled in the URL (usually included by default).

### Option B: Supabase

1. Create a new project.
2. Go to database connection settings.
3. Copy the PostgreSQL connection string.

## 4. Import Project in Vercel

1. Go to Vercel dashboard.
2. Click New Project.
3. Import your GitHub repository.
4. Keep root directory as repository root.
5. Deploy.

Vercel will use your existing `vercel.json` automatically.

## 5. Add Environment Variables in Vercel

In Vercel project settings, add these variables:

- `DJANGO_SECRET_KEY`
  - Use a long random value.
- `DJANGO_DEBUG`
  - Set to `False`
- `DJANGO_ALLOWED_HOSTS`
  - Example: `.vercel.app,your-domain.com`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
  - Example: `https://your-project.vercel.app,https://your-domain.com`
- `DATABASE_URL`
  - Your production PostgreSQL URL
- `RUN_MIGRATIONS`
  - Set to `1` for first deploy

After adding env vars, redeploy the project.

## 6. First Deployment Checklist

After deployment:

1. Open site URL and check homepage loads.
2. Open `/admin/` to verify Django admin route works.
3. Verify static assets load correctly (CSS/JS).
4. Confirm database tables are created.

## 7. Create Admin User (Superuser)

Run this from your local machine against the production database:

1. Export production database URL:
   - macOS/Linux:
     - `export DATABASE_URL='your-production-db-url'`
2. Run command:
   - `python3 manage.py createsuperuser`

This will create the admin user in the remote production database.

## 8. Migrations Strategy

Current setup runs migrations from `build_files.sh` only when:

- `RUN_MIGRATIONS=1`

Recommended workflow:

1. First deployment: keep `RUN_MIGRATIONS=1`
2. After successful migration: set it to `0` (or remove)
3. When you add new migrations later: temporarily set back to `1`, redeploy, then disable again

## 9. Important Limitation: Media Uploads

Vercel file system is ephemeral for serverless functions.

This means user-uploaded media stored on local disk is not persistent in production.

For persistent media, move uploads to cloud storage:
- Cloudinary
- AWS S3
- Supabase Storage

## 10. Troubleshooting

### DisallowedHost error

- Fix `DJANGO_ALLOWED_HOSTS`
- Include `.vercel.app` and your custom domain

### CSRF verification failed

- Fix `DJANGO_CSRF_TRUSTED_ORIGINS`
- Include full HTTPS origins, for example:
  - `https://your-project.vercel.app`

### Static files missing

- Ensure build completed successfully
- Ensure `collectstatic` is running (already in `build_files.sh`)
- Confirm `STATIC_ROOT` is `staticfiles`

### Database connection errors

- Verify `DATABASE_URL`
- Verify database allows external connections
- Verify SSL is enabled in connection string if required

## 11. Optional: Custom Domain

1. Add domain in Vercel project settings.
2. Update DNS records as instructed by Vercel.
3. Add your domain to:
   - `DJANGO_ALLOWED_HOSTS`
   - `DJANGO_CSRF_TRUSTED_ORIGINS`
4. Redeploy.

## 12. Quick Deploy Summary

1. Push code to GitHub
2. Import repo in Vercel
3. Add env vars
4. Set `RUN_MIGRATIONS=1`
5. Deploy
6. Create superuser
7. Disable migrations toggle (`RUN_MIGRATIONS=0`)

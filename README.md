# Django Photo Album Management

A production-ready Django photo album manager with Class-Based Views, role-based access control, Cloudinary media storage, and PostgreSQL support.

## Features
- Albums and photos with full CRUD functionality via CBVs
- Role-based administration using Django auth groups
- Cloudinary media upload integration
- PostgreSQL configuration via environment variables
- Render deployment support via `render.yaml` and `Procfile`

## Setup
1. Create a Python virtual environment and activate it.
2. Install packages: `pip install -r requirements.txt`
3. Configure environment variables:
   - `SECRET_KEY`
   - `DEBUG`
   - `DATABASE_URL`
   - `CLOUDINARY_URL`
   - `ALLOWED_HOSTS`
4. Run migrations: `python manage.py migrate`
5. Create a superuser: `python manage.py createsuperuser`
6. Run the development server: `python manage.py runserver`

## RBAC
- Standard authenticated users can browse albums and photo details.
- Users in the `album_admin` group or Django staff may create, edit, and delete albums and photos.

## Render Notes
- Use Render environment variables for credentials.
- Disable local media storage by using Cloudinary storage in production.

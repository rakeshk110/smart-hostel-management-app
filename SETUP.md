# Quick Setup Guide

## Step-by-Step Setup Instructions

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

**Note**: If `mysqlclient` installation fails on Windows, you can use:
```bash
pip install mysql-connector-python
```
Then update `settings.py` to use `'ENGINE': 'django.db.backends.mysql'` with `mysql-connector-python`.

### 2. Create MySQL Database
```sql
CREATE DATABASE smart_hostel_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Update Database Settings (if needed)
Edit `Smart_Hostel/settings.py` and update:
- `USER`: Your MySQL username (default: 'root')
- `PASSWORD`: Your MySQL password
- `HOST`: Your MySQL host (default: 'localhost')
- `PORT`: Your MySQL port (default: '3306')

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Admin User
```bash
python manage.py createsuperuser
```
Enter username, email, and password. Make sure to set `is_staff=True` for admin access.

### 6. Create Sample Data (Optional)
You can create sample data through Django admin at `/admin/`:
1. Create Rooms
2. Create Users (regular users for tenants)
3. Create Tenant profiles linking users to rooms
4. Create Bills for tenants

### 7. Run Server
```bash
python manage.py runserver
```

### 8. Access Application
- **Login Page**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Admin Dashboard**: http://127.0.0.1:8000/admin-dashboard/ (after admin login)
- **Tenant Dashboard**: http://127.0.0.1:8000/tenant-dashboard/ (after tenant login)

## User Roles

### Admin User
- Must have `is_staff=True` flag
- Can access admin dashboard
- Can manage rooms, bills, and complaints

### Tenant User
- Regular user (no staff flag)
- Can access tenant dashboard
- Can view bills, pay bills, and submit complaints

## Troubleshooting

### MySQL Connection Error
- Ensure MySQL server is running
- Verify database credentials in settings.py
- Check if database `smart_hostel_db` exists

### Static Files Not Loading
- Run: `python manage.py collectstatic`
- Check `STATIC_URL` and `STATICFILES_DIRS` in settings.py

### Migration Errors
- Delete migration files in `hostels/migrations/` (except `__init__.py`)
- Run `python manage.py makemigrations` again
- Run `python manage.py migrate`

### Template Not Found
- Ensure `templates/` directory is in project root
- Check `TEMPLATES` setting in `settings.py` includes `BASE_DIR / 'templates'`


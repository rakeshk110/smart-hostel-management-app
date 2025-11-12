# Smart Hostel Management System

A comprehensive Django-based web application for managing hostel operations including rooms, tenants, bills, and complaints.

## Features

### Admin Dashboard
- View total tenants, rooms, unpaid bills, and complaints
- CRUD operations for rooms
- CRUD operations for bills
- Update complaint status
- View detailed statistics and recent activities

### Tenant Dashboard
- View personal room information
- View monthly bills (paid/unpaid)
- Pay bills (mock payment functionality)
- Submit and track complaints
- View bill history

## Technology Stack

- **Backend**: Django 5.2.5
- **Database**: MySQL
- **Frontend**: HTML, CSS, Bootstrap 5
- **Language**: Python 3.x

## Installation

### Prerequisites

1. Python 3.x installed
2. MySQL server installed and running
3. pip (Python package manager)

### Setup Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure MySQL Database**
   - Create a MySQL database named `smart_hostel_db`
   - Update database credentials in `Smart_Hostel/settings.py` if needed:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'smart_hostel_db',
             'USER': 'root',
             'PASSWORD': 'your_password',
             'HOST': 'localhost',
             'PORT': '3306',
         }
     }
     ```

3. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create Superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   ```
   - This will create an admin user with staff privileges

5. **Create Tenant Users**
   - Use Django admin panel at `/admin/` to create regular users
   - Create Tenant profiles and link them to users and rooms

6. **Collect Static Files**
   ```bash
   python manage.py collectstatic
   ```

7. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

8. **Access the Application**
   - Open browser and navigate to `http://127.0.0.1:8000/`
   - Login with admin credentials to access admin dashboard
   - Login with tenant credentials to access tenant dashboard

## Project Structure

```
Smart_Hostel/
├── hostels/              # Main application
│   ├── models.py        # Database models (Room, Tenant, Bill, Complaint)
│   ├── views.py         # View functions
│   ├── urls.py          # URL routing
│   ├── forms.py         # Form definitions
│   └── admin.py         # Django admin configuration
├── templates/           # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── admin_dashboard.html
│   ├── tenant_dashboard.html
│   └── ...
├── static/              # Static files
│   └── css/
│       └── style.css
└── Smart_Hostel/        # Project settings
    ├── settings.py
    └── urls.py
```

## Models

### Room
- `room_number`: Unique room identifier
- `capacity`: Maximum number of tenants
- `rent`: Monthly rent amount

### Tenant
- `user`: OneToOne relationship with Django User
- `room`: ForeignKey to Room
- `join_date`: Date when tenant joined

### Bill
- `tenant`: ForeignKey to Tenant
- `month`: Month and year (e.g., "January 2024")
- `amount`: Bill amount
- `status`: Paid or Unpaid
- `paid_at`: Timestamp when bill was paid

### Complaint
- `tenant`: ForeignKey to Tenant
- `subject`: Complaint subject
- `message`: Detailed complaint message
- `status`: Pending or Resolved
- `resolved_at`: Timestamp when complaint was resolved

## URL Routes

### Authentication
- `/` or `/login/` - Login page
- `/logout/` - Logout

### Admin Routes
- `/admin-dashboard/` - Admin dashboard
- `/admin/rooms/` - List all rooms
- `/admin/rooms/create/` - Create new room
- `/admin/rooms/<id>/update/` - Update room
- `/admin/rooms/<id>/delete/` - Delete room
- `/admin/bills/` - List all bills
- `/admin/bills/create/` - Create new bill
- `/admin/bills/<id>/update/` - Update bill
- `/admin/bills/<id>/delete/` - Delete bill
- `/admin/complaints/` - List all complaints
- `/admin/complaints/<id>/update-status/` - Update complaint status

### Tenant Routes
- `/tenant-dashboard/` - Tenant dashboard
- `/bills/` - View all bills
- `/pay-bill/<id>/` - Pay a bill
- `/new-complaint/` - Submit new complaint

## Usage

### For Administrators

1. **Login** with admin credentials (staff user)
2. **View Dashboard** to see overview statistics
3. **Manage Rooms**: Create, update, or delete rooms
4. **Manage Bills**: Create bills for tenants, update or delete bills
5. **Handle Complaints**: View and update complaint status

### For Tenants

1. **Login** with tenant credentials (regular user)
2. **View Dashboard** to see personal information and bills
3. **Pay Bills**: Click "Pay Now" button on unpaid bills
4. **Submit Complaints**: Use "New Complaint" to submit issues
5. **View History**: Check bill history and complaint status

## Notes

- Bill payment is a mock implementation (updates status to "Paid")
- Admin users are identified by `is_staff=True` flag
- Regular users are treated as tenants
- Ensure MySQL server is running before starting the application
- For production, update `SECRET_KEY` and set `DEBUG=False` in settings.py

## License

This project is created for educational purposes.


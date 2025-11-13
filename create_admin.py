import os
import django

# Set the settings module for your project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Smart_Hostel.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='Rakesh').exists():
    User.objects.create_superuser('Rakesh', 'rakesh.kesavan30@gmail.com', 'Rakesh')
    print("✅ Superuser created successfully!")
else:
    print("ℹ️ Superuser already exists.")

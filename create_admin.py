from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('Rakesh','rakesh.kesavan30@gmail.com','Rakesh')
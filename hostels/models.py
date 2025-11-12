from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Room(models.Model):
    """
    Model to store room information
    """
    room_number = models.CharField(max_length=10, unique=True, help_text="Unique room number")
    capacity = models.IntegerField(validators=[MinValueValidator(1)], help_text="Maximum number of tenants")
    rent = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], help_text="Monthly rent amount")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['room_number']

    def __str__(self):
        return f"Room {self.room_number}"

    def get_current_tenants_count(self):
        """Returns the current number of tenants in this room"""
        return self.tenant_set.count()

    def is_full(self):
        """Checks if the room has reached its capacity"""
        return self.get_current_tenants_count() >= self.capacity


class Tenant(models.Model):
    """
    Model to store tenant information
    Links to Django's built-in User model for authentication
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tenant_profile')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='tenants')
    join_date = models.DateField(auto_now_add=True, help_text="Date when tenant joined the hostel")
    phone = models.CharField(max_length=15, blank=True, help_text="Contact phone number")
    address = models.TextField(blank=True, help_text="Permanent address")

    class Meta:
        ordering = ['user__first_name', 'user__last_name']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - Room {self.room.room_number if self.room else 'N/A'}"


class Bill(models.Model):
    """
    Model to store monthly bills for tenants
    """
    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='bills')
    month = models.CharField(max_length=20, help_text="Month and year (e.g., 'January 2024')")
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], help_text="Bill amount")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Unpaid')
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True, help_text="Date when bill was paid")

    class Meta:
        ordering = ['-month', '-created_at']
        unique_together = ['tenant', 'month']  # One bill per tenant per month

    def __str__(self):
        return f"{self.tenant.user.username} - {self.month} - {self.status}"


class Complaint(models.Model):
    """
    Model to store tenant complaints
    """
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='complaints')
    subject = models.CharField(max_length=200, help_text="Complaint subject")
    message = models.TextField(help_text="Detailed complaint message")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True, help_text="Date when complaint was resolved")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.tenant.user.username} - {self.subject} - {self.status}"

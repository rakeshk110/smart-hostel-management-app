from django.contrib import admin
from .models import Room, Tenant, Bill, Complaint


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """
    Admin interface for Room model
    """
    list_display = ['room_number', 'capacity', 'rent', 'get_current_tenants_count', 'is_full', 'created_at']
    list_filter = ['created_at']
    search_fields = ['room_number']
    readonly_fields = ['created_at', 'updated_at']

    def get_current_tenants_count(self, obj):
        """Display current number of tenants in the room"""
        return obj.get_current_tenants_count()
    get_current_tenants_count.short_description = 'Current Tenants'


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    """
    Admin interface for Tenant model
    """
    list_display = ['user', 'room', 'join_date', 'phone']
    list_filter = ['join_date', 'room']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone']
    readonly_fields = ['join_date']


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    """
    Admin interface for Bill model
    """
    list_display = ['tenant', 'month', 'amount', 'status', 'created_at', 'paid_at']
    list_filter = ['status', 'created_at', 'month']
    search_fields = ['tenant__user__username', 'month']
    readonly_fields = ['created_at', 'paid_at']


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    """
    Admin interface for Complaint model
    """
    list_display = ['tenant', 'subject', 'status', 'created_at', 'resolved_at']
    list_filter = ['status', 'created_at']
    search_fields = ['tenant__user__username', 'subject', 'message']
    readonly_fields = ['created_at', 'updated_at', 'resolved_at']

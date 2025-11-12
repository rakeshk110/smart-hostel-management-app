from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('', views.login_view, name='login_view'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register_view, name='register_view'),
    path('logout/', views.logout_view, name='logout_view'),

    # Dashboard URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('tenant-dashboard/', views.tenant_dashboard, name='tenant_dashboard'),

    # Tenant URLs
    path('pay-bill/<int:bill_id>/', views.pay_bill, name='pay_bill'),
    path('new-complaint/', views.new_complaint, name='new_complaint'),
    path('bills/', views.bill_list, name='bill_list'),

    # Admin Room CRUD URLs
    path('manage/rooms/', views.room_list, name='room_list'),
    path('manage/rooms/create/', views.room_create, name='room_create'),
    path('manage/rooms/<int:room_id>/update/', views.room_update, name='room_update'),
    path('manage/rooms/<int:room_id>/delete/', views.room_delete, name='room_delete'),

    # Admin Bill CRUD URLs
    path('manage/bills/', views.admin_bill_list, name='admin_bill_list'),
    path('manage/bills/create/', views.admin_bill_create, name='admin_bill_create'),
    path('manage/bills/<int:bill_id>/update/', views.admin_bill_update, name='admin_bill_update'),
    path('manage/bills/<int:bill_id>/delete/', views.admin_bill_delete, name='admin_bill_delete'),

    # Admin Complaint URLs
    path('manage/complaints/', views.admin_complaint_list, name='admin_complaint_list'),
    path('manage/complaints/<int:complaint_id>/update-status/', views.admin_complaint_update_status, name='admin_complaint_update_status'),

    # Admin Tenant Management URLs
    path('manage/tenants/', views.tenant_list, name='tenant_list'),
    path('manage/tenants/<int:tenant_id>/assign-room/', views.assign_room, name='assign_room'),
]


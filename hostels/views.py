from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.utils import timezone
from .models import Room, Tenant, Bill, Complaint
from .forms import ComplaintForm, RoomForm, BillForm, UserRegistrationForm, TenantRoomAssignmentForm


def register_view(request):
    """
    Handle user registration for tenants
    Creates a new user and associated tenant profile
    """
    if request.user.is_authenticated:
        # If user is already logged in, redirect based on their role
        if request.user.is_staff:
            return redirect('admin_dashboard')
        else:
            return redirect('tenant_dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create tenant profile
            phone = form.cleaned_data.get('phone', '')
            Tenant.objects.create(
                user=user,
                phone=phone
            )
            messages.success(request, 'Registration successful! Please login to continue.')
            return redirect('login_view')
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    """
    Handle user login for both admin and tenants
    Redirects admin to /admin-dashboard/ and tenant to /tenant-dashboard/
    """
    if request.user.is_authenticated:
        # If user is already logged in, redirect based on their role
        if request.user.is_staff:
            return redirect('admin_dashboard')
        else:
            return redirect('tenant_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect based on user role
            if user.is_staff:
                messages.success(request, f'Welcome, Admin {user.username}!')
                return redirect('admin_dashboard')
            else:
                messages.success(request, f'Welcome, {user.get_full_name() or user.username}!')
                return redirect('tenant_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


@login_required
def logout_view(request):
    """
    Handle user logout
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login_view')


@login_required
def admin_dashboard(request):
    """
    Admin dashboard showing overview statistics and management options
    Only accessible to staff users
    """
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('tenant_dashboard')

    # Calculate statistics
    total_tenants = Tenant.objects.count()
    total_rooms = Room.objects.count()
    unpaid_bills = Bill.objects.filter(status='Unpaid').count()
    pending_complaints = Complaint.objects.filter(status='Pending').count()

    # Get recent data
    recent_tenants = Tenant.objects.select_related('user', 'room').order_by('-join_date')[:5]
    recent_complaints = Complaint.objects.select_related('tenant__user').filter(status='Pending').order_by('-created_at')[:5]
    recent_bills = Bill.objects.select_related('tenant__user').filter(status='Unpaid').order_by('-created_at')[:5]

    # Get all rooms with tenant count
    rooms = Room.objects.annotate(tenant_count=Count('tenants')).all()

    context = {
        'total_tenants': total_tenants,
        'total_rooms': total_rooms,
        'unpaid_bills': unpaid_bills,
        'pending_complaints': pending_complaints,
        'recent_tenants': recent_tenants,
        'recent_complaints': recent_complaints,
        'recent_bills': recent_bills,
        'rooms': rooms,
    }

    return render(request, 'admin_dashboard.html', context)


@login_required
def tenant_dashboard(request):
    """
    Tenant dashboard showing personal room info, bills, and complaints
    """
    try:
        tenant = Tenant.objects.select_related('user', 'room').get(user=request.user)
    except Tenant.DoesNotExist:
        messages.error(request, 'Tenant profile not found. Please contact administrator.')
        return redirect('login_view')

    # Get tenant's bills
    bills = Bill.objects.filter(tenant=tenant).order_by('-month', '-created_at')
    paid_bills = bills.filter(status='Paid')
    unpaid_bills = bills.filter(status='Unpaid')

    # Get tenant's complaints
    complaints = Complaint.objects.filter(tenant=tenant).order_by('-created_at')

    # Calculate total amounts
    total_paid = paid_bills.aggregate(total=Sum('amount'))['total'] or 0
    total_unpaid = unpaid_bills.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'tenant': tenant,
        'bills': bills,
        'paid_bills': paid_bills,
        'unpaid_bills': unpaid_bills,
        'complaints': complaints,
        'total_paid': total_paid,
        'total_unpaid': total_unpaid,
    }

    return render(request, 'tenant_dashboard.html', context)


@login_required
def pay_bill(request, bill_id):
    """
    Handle bill payment (mock payment)
    Updates bill status to 'Paid' and sets paid_at timestamp
    """
    bill = get_object_or_404(Bill, id=bill_id)

    # Ensure only the bill owner can pay
    if bill.tenant.user != request.user:
        messages.error(request, 'You do not have permission to pay this bill.')
        return redirect('tenant_dashboard')

    if bill.status == 'Paid':
        messages.info(request, 'This bill has already been paid.')
        return redirect('tenant_dashboard')

    # Mock payment - update bill status
    bill.status = 'Paid'
    bill.paid_at = timezone.now()
    bill.save()

    messages.success(request, f'Bill for {bill.month} has been paid successfully!')
    return redirect('tenant_dashboard')


@login_required
def new_complaint(request):
    """
    Handle new complaint submission by tenants
    """
    try:
        tenant = Tenant.objects.get(user=request.user)
    except Tenant.DoesNotExist:
        messages.error(request, 'Tenant profile not found. Please contact administrator.')
        return redirect('login_view')

    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.tenant = tenant
            complaint.save()
            messages.success(request, 'Your complaint has been submitted successfully!')
            return redirect('tenant_dashboard')
    else:
        form = ComplaintForm()

    return render(request, 'new_complaint.html', {'form': form})


@login_required
def bill_list(request):
    """
    Display all bills for the logged-in tenant
    """
    try:
        tenant = Tenant.objects.get(user=request.user)
    except Tenant.DoesNotExist:
        messages.error(request, 'Tenant profile not found. Please contact administrator.')
        return redirect('login_view')

    bills = Bill.objects.filter(tenant=tenant).order_by('-month', '-created_at')

    context = {
        'bills': bills,
        'tenant': tenant,
    }

    return render(request, 'bill_list.html', context)


# Admin CRUD operations for Rooms
@login_required
def room_list(request):
    """
    List all rooms (Admin only)
    """
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('tenant_dashboard')

    rooms = Room.objects.annotate(tenant_count=Count('tenants')).all()
    return render(request, 'room_list.html', {'rooms': rooms})


@login_required
def room_create(request):
    """
    Create a new room (Admin only)
    """
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('tenant_dashboard')

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room created successfully!')
            return redirect('room_list')
    else:
        form = RoomForm()

    return render(request, 'room_form.html', {'form': form, 'title': 'Create Room'})


@login_required
def room_update(request, room_id):
    """
    Update an existing room (Admin only)
    """
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('tenant_dashboard')

    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room updated successfully!')
            return redirect('room_list')
    else:
        form = RoomForm(instance=room)

    return render(request, 'room_form.html', {'form': form, 'title': 'Update Room', 'room': room})


@login_required
def room_delete(request, room_id):
    """
    Delete a room (Admin only)
    """
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('tenant_dashboard')

    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Room deleted successfully!')
        return redirect('room_list')

    return render(request, 'room_confirm_delete.html', {'room': room})


# Admin CRUD operations for Bills
@login_required
def admin_bill_list(request):
    """
    List all bills (Admin only)
    """
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('tenant_dashboard')

    bills = Bill.objects.select_related('tenant__user', 'tenant__room').all().order_by('-created_at')
    return render(request, 'admin_bill_list.html', {'bills': bills})


@login_required
def admin_bill_create(request):
    """
    Create a new bill (Admin only)
    """
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('tenant_dashboard')

    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bill created successfully!')
            return redirect('admin_bill_list')
    else:
        form = BillForm()

    return render(request, 'bill_form.html', {'form': form, 'title': 'Create Bill'})


@login_required
def admin_bill_update(request, bill_id):
    """
    Update an existing bill (Admin only)
    """
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('tenant_dashboard')

    bill = get_object_or_404(Bill, id=bill_id)

    if request.method == 'POST':
        form = BillForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bill updated successfully!')
            return redirect('admin_bill_list')
    else:
        form = BillForm(instance=bill)

    return render(request, 'bill_form.html', {'form': form, 'title': 'Update Bill', 'bill': bill})


@login_required
def admin_bill_delete(request, bill_id):
    """
    Delete a bill (Admin only)
    """
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('tenant_dashboard')

    bill = get_object_or_404(Bill, id=bill_id)

    if request.method == 'POST':
        bill.delete()
        messages.success(request, 'Bill deleted successfully!')
        return redirect('admin_bill_list')

    return render(request, 'bill_confirm_delete.html', {'bill': bill})


# Admin operations for Complaints
@login_required
def admin_complaint_list(request):
    """
    List all complaints (Admin only)
    """
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('tenant_dashboard')

    complaints = Complaint.objects.select_related('tenant__user').all().order_by('-created_at')
    return render(request, 'admin_complaint_list.html', {'complaints': complaints})


@login_required
def admin_complaint_update_status(request, complaint_id):
    """
    Update complaint status (Admin only)
    """
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('tenant_dashboard')

    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Resolved']:
            complaint.status = new_status
            if new_status == 'Resolved':
                complaint.resolved_at = timezone.now()
            else:
                complaint.resolved_at = None
            complaint.save()
            messages.success(request, f'Complaint status updated to {new_status}!')
            return redirect('admin_complaint_list')

    return render(request, 'admin_complaint_update.html', {'complaint': complaint})


# Admin Tenant Management
@login_required
def tenant_list(request):
    """
    List all tenants (Admin only)
    """
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('tenant_dashboard')

    tenants = Tenant.objects.select_related('user', 'room').all().order_by('user__first_name', 'user__last_name')
    return render(request, 'tenant_list.html', {'tenants': tenants})


@login_required
def assign_room(request, tenant_id):
    """
    Assign or update room for a tenant (Admin only)
    """
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('tenant_dashboard')

    tenant = get_object_or_404(Tenant, id=tenant_id)

    if request.method == 'POST':
        form = TenantRoomAssignmentForm(request.POST, instance=tenant)
        if form.is_valid():
            # Check if the selected room has capacity
            selected_room = form.cleaned_data.get('room')
            if selected_room:
                current_count = selected_room.tenants.count()
                # If tenant is being moved from another room, don't count them in current room
                if tenant.room and tenant.room.id == selected_room.id:
                    # Tenant is staying in same room, no change needed
                    pass
                elif current_count >= selected_room.capacity:
                    messages.error(request, f'Room {selected_room.room_number} is already full!')
                    return render(request, 'assign_room.html', {'form': form, 'tenant': tenant})
            
            form.save()
            if selected_room:
                messages.success(request, f'Room {selected_room.room_number} assigned to {tenant.user.get_full_name() or tenant.user.username} successfully!')
            else:
                messages.success(request, f'Room unassigned from {tenant.user.get_full_name() or tenant.user.username} successfully!')
            return redirect('tenant_list')
    else:
        form = TenantRoomAssignmentForm(instance=tenant)

    return render(request, 'assign_room.html', {'form': form, 'tenant': tenant})

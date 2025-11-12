from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Count
from .models import Complaint, Room, Tenant, Bill


class UserRegistrationForm(UserCreationForm):
    """
    Form for user registration (tenants)
    """
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name',
            'required': True
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name',
            'required': True
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'required': True
        })
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number (optional)'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username',
                'required': True
            }),
        }
        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })


class ComplaintForm(forms.ModelForm):
    """
    Form for tenants to submit complaints
    """
    class Meta:
        model = Complaint
        fields = ['subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter complaint subject',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your complaint in detail...',
                'required': True
            }),
        }
        labels = {
            'subject': 'Subject',
            'message': 'Message',
        }


class RoomForm(forms.ModelForm):
    """
    Form for admin to create/edit rooms
    """
    class Meta:
        model = Room
        fields = ['room_number', 'capacity', 'rent']
        widgets = {
            'room_number': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'required': True
            }),
            'rent': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0,
                'required': True
            }),
        }


class BillForm(forms.ModelForm):
    """
    Form for admin to create/edit bills
    """
    class Meta:
        model = Bill
        fields = ['tenant', 'month', 'amount', 'status']
        widgets = {
            'tenant': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'month': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., January 2024',
                'required': True
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0,
                'required': True
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
        }


class TenantRoomAssignmentForm(forms.ModelForm):
    """
    Form for admin to assign/update room for tenants
    """
    class Meta:
        model = Tenant
        fields = ['room']
        widgets = {
            'room': forms.Select(attrs={
                'class': 'form-control',
                'required': False
            }),
        }
        labels = {
            'room': 'Assign Room',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get all rooms and filter available ones
        all_rooms = Room.objects.annotate(
            tenant_count=Count('tenants')
        ).all()
        
        available_room_ids = []
        current_room_id = None
        
        # Get current room ID if tenant has one
        if self.instance and self.instance.room:
            current_room_id = self.instance.room.id
        
        # Filter available rooms (not at capacity)
        for room in all_rooms:
            if room.tenant_count < room.capacity:
                available_room_ids.append(room.id)
            # Always include current room even if full (to allow viewing current assignment)
            elif current_room_id and room.id == current_room_id:
                available_room_ids.append(room.id)
        
        # Set queryset
        if available_room_ids:
            self.fields['room'].queryset = Room.objects.filter(id__in=available_room_ids)
        else:
            # If no available rooms, show all rooms (for viewing current assignment)
            self.fields['room'].queryset = Room.objects.all()
        
        # Add empty option
        self.fields['room'].empty_label = "No Room (Unassign)"


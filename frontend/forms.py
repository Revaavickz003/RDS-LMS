from django import forms
from .models import CustomUser, customertable

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'employee_mobile_number', 
            'position', 
            'document', 
            'date_of_birth', 
            'parent_number', 
            'employee_photo', 
            'qualification', 
            'company_email', 
            'date_of_join',
            'is_trainee', 
            'is_staff', 
            'is_teamlead', 
            'is_superuser',
            'address', 
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'employee_mobile_number': forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
            'parent_number': forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'employee_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'company_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'date_of_join': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows':'3'}),
            'is_trainee': forms.CheckboxInput(attrs={'class': 'form-check-input mx-1','type':'checkbox'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input mx-1','type':'checkbox'}),
            'is_teamlead': forms.CheckboxInput(attrs={'class': 'form-check-input mx-1','type':'checkbox'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input mx-1','type':'checkbox'}),
        }

class customertableForm(forms.ModelForm):
    class Meta:
        model = customertable
        fields = '__all__'

from django import forms
from import_export.forms import ImportForm
from .models import Lead

class LeadImportForm(ImportForm):
    class Meta:
        model = Lead
        fields = (
            'client_name',
            'client_number',
            'org_name',
            'org_img',
            'org_type',
            'location',
            'city',
            'lead_name',
            'business_type',
            'products',
            'amount',
            'end_of_date',
            'priority',
            'mail_id',
            'status',
            'comment',
            'remarks',
            'follow_up',
        )
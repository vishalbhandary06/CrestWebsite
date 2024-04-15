from tabnanny import verbose
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import *

class AddEmployeeForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = ('email', 'first_name', 'emp_id', 'password1', 'password2', 'role',)


    #     widgets = {
    #         'email' : forms.EmailInput(attrs={'class' : 'form-control form-control-lg'}),
    #         'first_name' : forms.TextInput(attrs={'class' : 'form-control form-control-lg'}),
    #         'emp_id' : forms.TextInput(attrs={'class' : 'form-control form-control-lg'}),
    #         'position' : forms.Select(attrs={'class' : 'form-select form-select-lg'}),
    #     }

    # def __init__(self, *args, **kwargs):
    #     super(AddEmployeeForm, self).__init__(*args, **kwargs)
    #     self.fields['password1'].widget.attrs['class'] = 'form-control form-control-lg'
    #     self.fields['password2'].widget.attrs['class'] = 'form-control form-control-lg'

class EmployeeAuthentiationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    class Meta:
        model = Employee
        fields = ('email', 'password')

        widgets = {
            'email' : forms.EmailInput(attrs={'class' : 'form-control col'}),
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeAuthentiationForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['class'] = 'form-control'

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Login")


class EmployeePersonalUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('email', 'first_name', 'last_name', 'gender', 'birthday', 'phone', 'per_email', 'marital', 'blood', 'c_address', 'p_address',)

        # widgets = {
        #     'email' : forms.EmailInput(attrs={'class' : 'form-control form-control-lg'}),
        #     'per_email' : forms.EmailInput(attrs={'class' : 'form-control form-control-lg'}),
        #     'first_name' : forms.TextInput(attrs={'class' : 'form-control form-control-lg'}),
        #     'last_name' : forms.TextInput(attrs={'class' : 'form-control form-control-lg'}),
        #     'phone' : forms.TextInput(attrs={'class' : 'form-control form-control-lg'}),
        #     'c_address' : forms.Textarea(attrs={'class' : 'form-control form-control-lg', 'style' : 'height: 200px;'}),
        #     'p_address' : forms.Textarea(attrs={'class' : 'form-control form-control-lg'}),
        #     'gender' : forms.Select(attrs={'class' : 'form-select form-select-lg'}),
        #     'marital' : forms.Select(attrs={'class' : 'form-select form-select-lg'}),
        #     'blood' : forms.Select(attrs={'class' : 'form-select form-select-lg'}),
        #     'birthday' : forms.TextInput(attrs={'class' : 'form-control form-control-lg'}),
        # }

        widgets = {
            'c_address' : forms.Textarea(attrs={'class' : 'form-control', 'style' : 'height: 150px;'}),
            'p_address' : forms.Textarea(attrs={'class' : 'form-control', 'style' : 'height: 150px;'}),
        }

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                employee = Employee.objects.exclude(pk=self.instance.pk).get(email=email)
            except Employee.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" is already in use.' % employee.email)

    # def clean(self):
    #     if self.is_valid():
    #         first_name = self.cleaned_data['first_name']
    #         last_name = self.cleaned_data['last_name']
    #         gender = self.cleaned_data['gender']
    #         birthday = self.cleaned_data['birthday']
    #         c_address = self.cleaned_data['c_address']
    #         p_address = self.cleaned_data['p_address']
    #         phone = self.cleaned_data['phone']
    #         per_email = self.cleaned_data['per_email']
    #         marital = self.cleaned_data['marital']
    #         blood = self.cleaned_data['blood']

class EmployeeWorkUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('emp_id', 'emp_status', 'department', 'manager', 'role', 'title', 'position', 'experience', 'is_active')

class EmployeeTeamUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('email', 'first_name', 'last_name', 'gender', 'birthday', 'emp_id', 'position',)

        widgets = {
            'email' : forms.EmailInput(attrs={'class' : 'form-control form-control-lg'}),
            'first_name' : forms.TextInput(attrs={'class' : 'form-control form-control-lg'}),
            'last_name' : forms.TextInput(attrs={'class' : 'form-control form-control-lg'}),
            'gender' : forms.Select(attrs={'class' : 'form-select form-select-lg'}),
            'birthday' : forms.TextInput(attrs={'class' : 'form-control form-control-lg'}),
            'emp_id' : forms.TextInput(attrs={'class' : 'form-control form-control-lg'}),
            'position' : forms.Select(attrs={'class' : 'form-select form-select-lg'}),
        }

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                employee = Employee.objects.exclude(pk=self.instance.pk).get(email=email)
            except Employee.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" is already in use.' % employee.email)

    def clean(self):
        if self.is_valid():
            first_name = self.cleaned_data['first_name']
            last_name = self.cleaned_data['last_name']
            gender = self.cleaned_data['gender']
            emp_id = self.cleaned_data['emp_id']
            position = self.cleaned_data['position']

class ChangePasswordForm(UserCreationForm):
    password = forms.CharField(label="Old Password", widget=forms.PasswordInput())
    class Meta:
        model = Employee
        fields = ('password','password1', 'password2',)

class RelationshipForm(forms.ModelForm):
    class Meta:
        model = Relationship
        exclude = ['employee']

class EmergencyForm(forms.ModelForm):
    class Meta:
        model = Emergency
        exclude = ['employee']

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ['employee']

        widgets = {
            'start' : forms.TextInput(attrs={'class' : 'form-select'}),
            'end' : forms.TextInput(attrs={'class' : 'form-select'}),
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name',)

class TitleForm(forms.ModelForm):
    class Meta:
        model = Title
        fields = ('name',)

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ('name',)

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ('name', 'priority',)
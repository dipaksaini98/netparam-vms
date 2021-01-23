from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Employee, Visit, Visitor


class EmployeeCreationForm(UserCreationForm):

    class Meta:
        model = Employee
        fields = ('username', 'name', 'email', 'contact', 'password1',
                  'password2', 'address', 'designation')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter Username'}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'abc@xyz.com'}),
            'contact': forms.TextInput(attrs={'placeholder': 'Contact'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address'}),
            'designation': forms.Select(choices=Employee.DESIGNATION),
        }


class EmployeeChangeForm(UserChangeForm):

    class Meta:
        model = Employee
        fields = ('username', 'name', 'email',
                  'contact', 'address', 'designation')


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = '__all__'


class AddVisitorForm(forms.ModelForm):
    date_visited = forms.DateField(
        widget=forms.DateInput(attrs={'placeholder': 'dd/mm/yyyy'}))

    class Meta:
        model = Visitor
        fields = '__all__'

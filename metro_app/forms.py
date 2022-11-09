import re

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateInput

from metro_app.models import Login, Trainer, Physician, Equipments, Customer, Batch, Complaint, Dietplan, Attendance, \
    Health, Notification, Payment


def phone_number_validator(value):
    if not re.compile(r'^[7-9]\d{9}$').match(value):
        raise ValidationError('this is not a valid phone number')


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class LoginForm(UserCreationForm):
    class Meta:
        model = Login
        fields = ('username', 'password1', 'password2')


class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ('name', 'address', 'contact_no', 'qualification', 'achievement', 'image', 'age')


class PhysicianForm(forms.ModelForm):
    class Meta:
        model = Physician
        fields = ('name', 'address', 'contact_no', 'qualification', 'image', 'age')


class EquipmentsForm(forms.ModelForm):
    class Meta:
        model = Equipments
        fields = ('name', 'image', 'description')


class CustomerForm(forms.ModelForm):
    contact_no = forms.CharField(validators=[phone_number_validator])

    class Meta:
        model = Customer
        fields = ('name', 'age', 'address', 'contact_no', 'image')


class BatchForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput)
    time = forms.TimeField(widget=TimeInput)

    class Meta:
        model = Batch
        fields = ('name', 'time', 'date')


class ComplaintForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput)

    class Meta:
        model = Complaint
        fields = ('complaint', 'date')


class DietplanForm(forms.ModelForm):
    class Meta:
        model = Dietplan
        fields = ('subject', 'image')


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('name', 'attendance', 'date', 'time')


class HealthForm(forms.ModelForm):
    class Meta:
        model = Health
        fields = ('name', 'height', 'weight', 'healthcondition', 'medicineconsuption',)


class NotificationForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput)

    class Meta:
        model = Notification
        fields = ('date', 'subject', 'text')


class PaymentForm(forms.ModelForm):
    due_date = forms.DateField(widget=DateInput)

    class Meta:
        model = Payment
        fields = ('name', 'amount', 'due_date')

from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_file_extension, content_file_name
from .managers import CustomUserManager
# Create your models here.


class Employee(AbstractUser):
    DESIGNATION = [("HR", "HR"), ("Employee", "Employee")]

    name = models.CharField(max_length=150, null=True)
    email = models.EmailField(max_length=100)
    contact = models.CharField(max_length=25, null=True)
    address = models.CharField(max_length=250, null=True)
    designation = models.CharField(
        max_length=50, choices=DESIGNATION, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.name


class Visitor(models.Model):
    CATEGORY = (('Student', 'Student'), ('Guest', 'Guest'))

    name = models.CharField(max_length=150, null=True)
    contact = models.CharField(max_length=20, null=True, unique=False)
    email = models.EmailField(max_length=100, null=True, unique=False)
    purpose = models.CharField(max_length=250, null=True)
    photo = models.ImageField(
        upload_to=content_file_name, validators=[validate_file_extension], null=True)
    category = models.CharField(max_length=50, choices=CATEGORY, null=True)
    date_visited = models.DateTimeField(auto_now_add=True, null=True)
    host = models.OneToOneField(Employee, null=True,
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Visit(models.Model):
    STATUS = (('Pending', 'Pending'), ('Done', 'Done'))
    employee = models.ForeignKey(
        Employee, null=True, on_delete=models.CASCADE)

    visitor = models.OneToOneField(
        Visitor, null=True, on_delete=models.CASCADE)

    date_visited = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=100, null=True, choices=STATUS)

    def __str__(self):
        return self.visitor.name


class Event(models.Model):
    event_name = models.CharField(max_length=250)
    event_date = models.DateTimeField()

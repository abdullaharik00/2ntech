from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password

ANNIAL_LEAVE_DAY = 15
OFFICE_START_HOUR = datetime.strptime("08:00", "%H:%M")
OFFICE_END_HOUR = datetime.strptime("18:00", "%H:%M")
DAILY_WORK_HOURS = (OFFICE_END_HOUR - OFFICE_START_HOUR).total_seconds() / 3600
ANNUAL_LEAVE_MINUTES = (OFFICE_END_HOUR.hour - OFFICE_START_HOUR.hour) * ANNIAL_LEAVE_DAY * 60

class User(AbstractUser):
    ROLES = (
        ('EMPLOYEE', 'Employee'),
        ('MANAGER', 'Manager'),
    )
    user_name = models.CharField(max_length=10,)
    role = models.CharField(max_length=10, choices=ROLES, default='EMPLOYEE')
    annual_leave_minutes = models.FloatField(default=ANNUAL_LEAVE_MINUTES)
    
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=False)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    late_minutes = models.PositiveIntegerField(default=0)

    def calculate_late_minutes(self):
        if self.check_in_time and self.check_in_time > OFFICE_START_HOUR.time():
            delta = datetime.combine(datetime.today(), self.check_in_time) - datetime.combine(datetime.today(), OFFICE_START_HOUR.time())
            self.late_minutes = delta.seconds // 60
            self.save()
            
            if self.user.annual_leave_minutes >= self.late_minutes:
                self.user.annual_leave_minutes -= self.late_minutes
                self.user.save()
            else:
                self.user.annual_leave_minutes = 0
                self.user.save()


class LeaveRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    @property
    def total_days(self):
        return (self.end_date - self.start_date).days + 1

from rest_framework import serializers
from .models import DAILY_WORK_HOURS, User, Attendance, LeaveRequest

class UserSerializer(serializers.ModelSerializer):
    remaining_leave = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'user_name', 'role', 'annual_leave_minutes', 'remaining_leave']

    def get_remaining_leave(self, obj):
        total_minutes = obj.annual_leave_minutes
        total_hours = total_minutes // 60
        total_days = total_hours // DAILY_WORK_HOURS
        remaining_hours = total_hours % DAILY_WORK_HOURS
        remaining_minutes = total_minutes % 60

        return f"{total_days} days, {remaining_hours} hours, {remaining_minutes} minutes"

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'user', 'date', 'check_in_time', 'check_out_time', 'late_minutes']

class LeaveRequestSerializer(serializers.ModelSerializer):
    total_days = serializers.ReadOnlyField()

    class Meta:
        model = LeaveRequest
        fields = ['id', 'user', 'start_date', 'end_date', 'status', 'total_days']

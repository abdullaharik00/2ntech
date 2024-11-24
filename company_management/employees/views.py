import json
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import (
    User,
    Attendance,
    LeaveRequest,
    OFFICE_START_HOUR,
    OFFICE_END_HOUR,
    DAILY_WORK_HOURS,
)
from .serializers import UserSerializer, AttendanceSerializer, LeaveRequestSerializer
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework import permissions
from django.utils.timezone import now
from datetime import datetime


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "MANAGER"


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsManager]


class AttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsManager]


class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsManager]

    def perform_create(self, serializer):
        user = serializer.validated_data["user"]
        leave_days = (
            serializer.validated_data["end_date"]
            - serializer.validated_data["start_date"]
        ).days + 1
        if user.annual_leave_hours < leave_days:
            raise serializers.ValidationError("Yeterli izin bulunmamaktadır.")
        user.annual_leave_hours -= leave_days
        user.save()
        serializer.save(user=user)


def attendance_date(request):
    user = request.user
    date = now().date()

    attendance = Attendance.objects.filter(user=user, date=date).first()
    if not attendance:
        attendance = Attendance.objects.create(user=user, date=date)
        if not attendance.check_in_time:
            attendance.check_in_time = now().time()
        attendance.calculate_late_minutes()

        attendance.save()


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.role == "EMPLOYEE":
                attendance_date(request)
                return redirect("employee_dashboard")
            elif user.role == "MANAGER":
                attendance_date(request)
                return redirect("manager_dashbord")
            else:
                return render(
                    request,
                    "login/login.html",
                    {
                        "error": "User does not belong to any group",
                    },
                )
        else:
            return render(request, "login/login.html", {"error": "Invalid credentials"})
    return render(request, "login/login.html")


@login_required
def logout_view(request):
    today = now().date()
    attendance = Attendance.objects.filter(user=request.user, date=today).first()

    if attendance and not attendance.check_out_time:
        attendance.check_out_time = now().time()
        attendance.save()
    logout(request)
    return redirect("login")


@login_required
def employee_dashboard(request):
    return render(request, "employee/dashboard.html")


@login_required
def manager_dashbord(request):
    return render(request, "manager/dashboard.html")


@login_required
def manager_attendance_dashboard(request):
    return render(request, "manager/manager_attendance_dashboard.html")

@login_required
def leave_request_management(request):
    return render(request, "manager/leave_request_management.html")


@login_required
def user_info(request):
    user = request.user

    total_minutes = user.annual_leave_minutes
    total_hours = total_minutes // 60
    
    total_days = total_hours // DAILY_WORK_HOURS

    remaining_hours = total_hours % DAILY_WORK_HOURS
    remaining_minutes = total_minutes % 60

    current_hour = now().hour
    # if not (OFFICE_START_HOUR.hour <= current_hour < OFFICE_END_HOUR.hour):
    #     return JsonResponse(
    #         {"error": "This information is only accessible during office hours."},
    #         status=403,
    #     )
    
    return JsonResponse(
        {
            "username": user.username,
            "role": user.role,
            "remaining_leave": f"{total_days} days, {remaining_hours} hours, {remaining_minutes} minutes",
        }
    )


@login_required
def all_users_info_attendance(request):
    user_data = []

    attendances = Attendance.objects.all()

    for attendance in attendances:
        date = attendance.date
        check_in_time = attendance.check_in_time
        check_out_time = attendance.check_out_time
        username = attendance.user.username
        
        if check_in_time:
            late_hours = attendance.late_minutes // 60
            late_remaining_minutes = attendance.late_minutes % 60
            late_time = f"{late_hours} hours {late_remaining_minutes} minutes" if attendance.late_minutes > 0 else "On time"
        else:
            late_time = "Not Checked In"

        user_data.append({
            "username": username,
            "date": date,
            "check_in_time": check_in_time.strftime("%H:%M") if check_in_time else "N/A",
            "check_out_time": check_out_time.strftime("%H:%M") if check_out_time else "N/A",
            "late_time": late_time,
        })

    return JsonResponse({"users": user_data})

########## İzin isteği

def handle_error(message, status=400):
    """Helper function to return a standardized error response."""
    return JsonResponse({'error': message}, status=status)


@login_required
def leave_requests(request):
    if request.method == 'GET':
        return get_leave_requests(request)
    
    elif request.method == 'POST':
        return create_leave_request(request)
    
    return handle_error('Method Not Allowed', status=405)


def get_leave_requests(request):
    user = request.user
    leave_requests = LeaveRequest.objects.filter(user=user).values('start_date', 'end_date', 'status')

    return JsonResponse({'leave_requests': list(leave_requests)})


def create_leave_request(request):
    try:
        data = json.loads(request.body)

        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')

        start_date, end_date = validate_dates(start_date_str, end_date_str)
        if isinstance(start_date, JsonResponse):
            return start_date

        if end_date < start_date:
            return handle_error('End date cannot be earlier than start date.')

        return create_new_leave_request(request.user, start_date, end_date)

    except (ValueError, KeyError) as e:
        return handle_error('Invalid data provided.')

    
def validate_dates(start_date_str, end_date_str):
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        return start_date, end_date
    except (ValueError, TypeError):
        return handle_error('Invalid date format. Expected format is YYYY-MM-DD.')


def create_new_leave_request(user, start_date, end_date):
    existing_pending_request = LeaveRequest.objects.filter(
        user=user,
        start_date=start_date,
    ).exists()

    if existing_pending_request:
        return handle_error('You already have a pending leave request for this day.')

    leave_request = LeaveRequest.objects.create(
        user=user,
        start_date=start_date,
        end_date=end_date,
        status='PENDING'
    )

    return JsonResponse({
        'message': 'Leave request created successfully',
        'leave_request': {
            'start_date': leave_request.start_date,
            'end_date': leave_request.end_date,
            'status': leave_request.status
        }
    })
    
    
    
    
    
    
    
@login_required
def get_leave_requests(request):
    """
    Retrieve all leave requests grouped by their status.
    """
    if request.method != 'GET':
        return handle_error('Only GET requests are allowed.', status=405)

    pending_requests = LeaveRequest.objects.filter(status='PENDING').values(
        'id', 'user__username', 'start_date', 'end_date'
    )
    approved_requests = LeaveRequest.objects.filter(status='APPROVED').values(
        'id', 'user__username', 'start_date', 'end_date'
    )
    rejected_requests = LeaveRequest.objects.filter(status='REJECTED').values(
        'id', 'user__username', 'start_date', 'end_date'
    )

    return JsonResponse({
        'pending': list(pending_requests),
        'approved': list(approved_requests),
        'rejected': list(rejected_requests),
    })


@login_required
def manage_leave_request(request, request_id):
    if request.method != 'POST':
        return handle_error('Only POST requests are allowed.', status=405)

    try:
        data = json.loads(request.body)
        action = data.get('action')

        if action not in ['approve', 'reject']:
            return handle_error('Invalid action. Use "approve" or "reject".')

        leave_request = LeaveRequest.objects.get(id=request_id)

        if leave_request.status != 'PENDING':
            return handle_error('Only pending requests can be managed.')

        if action == 'approve':
            return approve_leave_request(leave_request)
        elif action == 'reject':
            leave_request.status = 'REJECTED'
            leave_request.save()
            return JsonResponse({'message': 'Leave request rejected.'})

    except LeaveRequest.DoesNotExist:
        return handle_error('Leave request not found.', status=404)
    except KeyError:
        return handle_error('Invalid data provided.')


def approve_leave_request(leave_request):
    total_days = (leave_request.end_date - leave_request.start_date).days + 1
    user = leave_request.user
    
    total_minutes = total_days * DAILY_WORK_HOURS * 60

    if user.annual_leave_minutes < total_minutes:
        return handle_error('Insufficient leave balance.')

    user.annual_leave_minutes -= total_minutes
    user.save()

    leave_request.status = 'APPROVED'
    leave_request.save()

    return JsonResponse({'message': 'Leave request approved.'})
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import login_view, logout_view, employee_dashboard, manager_dashbord, manager_attendance_dashboard, leave_request_management


urlpatterns = [
    # path('', login_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('employee/', employee_dashboard, name='employee_dashboard'),
    path('manager/', manager_dashbord, name='manager_dashbord'),
    path('manager/attendance-dashboard/', manager_attendance_dashboard, name='manager_attendance_dashboard'),
    path('manager/leave-request-management/', leave_request_management, name='leave_request_management'),
]

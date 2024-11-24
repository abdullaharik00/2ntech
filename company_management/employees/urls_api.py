from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AttendanceViewSet, LeaveRequestViewSet, user_info, leave_requests, all_users_info_attendance, manage_leave_request

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('attendance', AttendanceViewSet)
router.register('leaves', LeaveRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user-info/', user_info, name='user_info'),
    path('all-users-info-attendance/', all_users_info_attendance, name='all_users_info_attendance'),
    path('leave-requests/', leave_requests, name='leave_requests'),
    path('manage-leave-request/<int:request_id>/', manage_leave_request, name='manage_leave_request'),
]

"""
URL configuration for company_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from employees.models import User, Attendance, LeaveRequest

admin.site.register(User)
admin.site.register(Attendance)
admin.site.register(LeaveRequest)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('employees.urls')),
    path('api/', include('employees.urls_api')),
]



# from django.contrib.auth.admin import UserAdmin
# 
# 
# class CustomUserAdmin(UserAdmin):
#     fieldsets = (
#         (None, {'fields': ('username', 'password', 'user_name', 'role', 'annual_leave_hoursw')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'password1', 'password2', 'role'),
#         }),
#     )
# 
#     def save_model(self, request, obj, form, change):
#         if form.cleaned_data.get('password'):
#             obj.set_password(form.cleaned_data['password'])  # Şifreyi hashle
#         super().save_model(request, obj, form, change)
# 
# admin.site.register(User, CustomUserAdmin)
"""school_managementPro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from school_managementapp import views, Hod_Views, Staff_Views, Student_Views

urlpatterns = [
    path('', views.showlogin,name='showlogin'),
    path('home/',views.home),
    path('showlogin/',views.showlogin),
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('dologin',views.dologin,name='dologin'),
    path('logout_user/',views.logout_user),
    path('get_user_details',views.GetUserDetails),
    path('logout/',views.logout_user),
    path('admin_home/',Hod_Views.admin_home,name='admin_home'),
    path('add_staff/',Hod_Views.add_staff),
    path('save_staff',Hod_Views.save_staff),
    path('manage_staff/',Hod_Views.manage_staff,name='manage_staff'),
    path('add_courses/',Hod_Views.add_courses),
    path('save_courses',Hod_Views.save_courses),
    path('manage_course/',Hod_Views.manage_course,name='manage_course'),
    path('add_students/',Hod_Views.add_students),
    path('save_students',Hod_Views.save_students),
    path('manage_student/',Hod_Views.manage_student,name='manage_student'),
    path('add_subjects/',Hod_Views.add_subjects),
    path('save_subjects',Hod_Views.save_subjects),
    path('manage_subject/',Hod_Views.manage_subject,name='manage_subject'),
    path('edit_student/<int:student_id>',Hod_Views.edit_student),
    path('save_edit_student',Hod_Views.save_edit_student),
    path('edit_staff/<int:staff_id>',Hod_Views.edit_staff),
    path('save_edit_staff',Hod_Views.save_edit_staff),
    path('edit_course/<int:course_id>',Hod_Views.edit_course),
    path('save_edit_course',Hod_Views.save_edit_course),
    path('edit_subject/<int:subject_id>',Hod_Views.edit_subject),
    path('save_edit_subject',Hod_Views.save_edit_subject),
    path('manage_session/',Hod_Views.manage_session),
    path('save_session',Hod_Views.save_session),
    path('hod_student_feedback',Hod_Views.hod_student_feedback),
    path('save_hod_student_feedback/<int:feedback_id>',Hod_Views.save_hod_student_feedback),
    path('hod_staff_feedback',Hod_Views.hod_staff_feedback),
    path('save_hod_staff_feedback/<int:feedback_id>',Hod_Views.save_hod_staff_feedback),
    path('hod_student_leave',Hod_Views.hod_student_leave),
    path('student_approve_leave/<int:leave_id>',Hod_Views.student_approve_leave),
    path('student_disapprove_leave/<int:leave_id>',Hod_Views.student_disapprove_leave),
    path('hod_staff_leave', Hod_Views.hod_staff_leave),
    path('staff_approve_leave/<int:leave_id>', Hod_Views.staff_approve_leave),
    path('staff_disapprove_leave/<int:leave_id>', Hod_Views.staff_disapprove_leave),


    # .......... .staff url         stafff url              STAFF  URL ...........
    path('staff_home/',Staff_Views.staff_home),
    path('take_attendance/',Staff_Views.take_attendance,name='take_attendance'),
    path('staff_update_attendance', Staff_Views.staff_update_attendance, name="staff_update_attendance"),
    path('get_attendance_dates', Staff_Views.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_student', Staff_Views.get_attendance_student, name="get_attendance_student"),
    path('save_attendance_data', Staff_Views.save_attendance_data, name="save_attendance_data"),
    path('save_updateattendance_data', Staff_Views.save_updateattendance_data, name="save_updateattend"),
    path('get_students',Staff_Views.get_students,name='get_students'),
    path('staff_apply_leave',Staff_Views.staff_apply_leave,name='staff_apply_leave'),
    path('save_staff_leave',Staff_Views.save_staff_leave,name='save_staff_leave'),
    path('feedback_staff',Staff_Views.feedback_staff,name='feedback_staff'),
    path('save_feedback_staff',Staff_Views.save_feedback_staff,name='save_feedback_staff'),
    path('staff_notification',Staff_Views.staff_notification,name='staff_notification'),
    # .............student url ............STUDENT URL.......
    path('student_home',Student_Views.student_home),
    path('student_apply_leave',Student_Views.student_apply_leave),
    path('save_student_leave',Student_Views.save_student_leave),
    path('student_feedback/',Student_Views.student_feedback),
    path('save_feedback_student',Student_Views.save_feedback_student),
    path('student_notification',Student_Views.student_notification),
    ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from school_managementapp.models import Students, LeaveReportStudent, FeedbackStudent, NotificationStuden


def student_home(request):
    return render(request,'student_templates/main_content_student.html')


def student_apply_leave(request):
    student_obj=Students.objects.get(admin=request.user.id)
    leave_history=LeaveReportStudent.objects.filter(student_id=student_obj)
    return render(request,'student_templates/student_apply_leave.html',{'leave_history':leave_history})


def save_student_leave(request):
    if request.method=='POST':
        leave_date=request.POST.get('leave_date')
        leave_reason=request.POST.get('leave_msg')
        student_obj=Students.objects.get(admin=request.user.id)
        try:
            student_leave = LeaveReportStudent(student_id=student_obj, leave_date=leave_date, leave_message=leave_reason,
                                           leave_status=0)
            student_leave.save()
            messages.success(request,'Successfully Applyed For Leave')
            return HttpResponseRedirect('student_apply_leave')
        except:
            messages.error(request, 'Failed to Apply For Leave')
            return HttpResponseRedirect('student_apply_leave')
    else:
        return HttpResponseRedirect(reverse('student_apply_leave'))


def student_feedback(request):
    stu_obj=Students.objects.get(admin=request.user.id)
    feedback=FeedbackStudent.objects.filter(student_id=stu_obj)
    return render(request,'student_templates/student_feedback.html',{'feedback':feedback})

def save_feedback_student(request):
    if request.method=="POST":
        feedback_msg=request.POST.get('feedback_msg')
        stu_obj=Students.objects.get(admin=request.user.id)
        try:
            feedback_model=FeedbackStudent(feedback=feedback_msg,student_id=stu_obj)
            feedback_model.save()
            messages.success(request,'Successfully Saved Feedback')
            return HttpResponseRedirect('student_feedback')
        except:
            messages.error(request,'Failed to save Feedback')
            return HttpResponseRedirect('student_feedback')
    else:
        return HttpResponseRedirect(reverse('student_feedback'))

def student_notification(request):
    stu_obj=Students.objects.get(admin=request.user.id)
    notifications=NotificationStuden.objects.filter(student_id=stu_obj)
    return render(request,'student_templates/student_notification.html',{'notifications':notifications})
from datetime import datetime

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from school_managementapp.models import CustomUser, Courses, Subjects, Staffs, Students, SessionYearModel, \
    FeedbackStudent, FeedbackStaffs, LeaveReportStudent, LeaveReportStaff, AttendanceReport, Attendance


def admin_home(request):
    student_count1=Students.objects.all().count()
    staff_count=Staffs.objects.all().count()
    subject_count=Subjects.objects.all().count()
    course_count=Courses.objects.all().count()

    course_all=Courses.objects.all()
    course_name_list=[]
    subject_count_list=[]
    student_count_list_in_course=[]
    for course in course_all:
        subjects=Subjects.objects.filter(course_id=course.id).count()
        students=Students.objects.filter(courese_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)

    subjects_all=Subjects.objects.all()
    subject_list=[]
    student_count_list_in_subject=[]
    for subject in subjects_all:
        course=Courses.objects.get(id=subject.course_id.id)
        student_count=Students.objects.filter(courese_id=course.id).count()
        subject_list.append(subject.subject)
        student_count_list_in_subject.append(student_count)

    staffs=Staffs.objects.all()
    attendance_present_list_staff=[]
    attendance_absent_list_staff=[]
    staff_name_list=[]
    for staff in staffs:
        subject_ids=Subjects.objects.filter(stuff_id=staff.admin.id)
        attendance=Attendance.objects.filter(subject_id__in=subject_ids).count()
        leaves=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
        attendance_present_list_staff.append(attendance)
        attendance_absent_list_staff.append(leaves)
        staff_name_list.append(staff.admin.username)

    students_all=Students.objects.all()
    attendance_present_list_student=[]
    attendance_absent_list_student=[]
    student_name_list=[]
    for student in students_all:
        attendance=AttendanceReport.objects.filter(student_id=student.id,status=True).count()
        absent=AttendanceReport.objects.filter(student_id=student.id,status=False).count()
        leaves=LeaveReportStudent.objects.filter(student_id=student.id,leave_status=1).count()
        attendance_present_list_student.append(attendance)
        attendance_absent_list_student.append(leaves+absent)
        student_name_list.append(student.admin.username)


    return render(request,"hod_templates/home_content.html",{"student_count":student_count1,"staff_count":staff_count,"subject_count":subject_count,"course_count":course_count,"course_name_list":course_name_list,"subject_count_list":subject_count_list,"student_count_list_in_course":student_count_list_in_course,"student_count_list_in_subject":student_count_list_in_subject,"subject_list":subject_list,"staff_name_list":staff_name_list,"attendance_present_list_staff":attendance_present_list_staff,"attendance_absent_list_staff":attendance_absent_list_staff,"student_name_list":student_name_list,"attendance_present_list_student":attendance_present_list_student,"attendance_absent_list_student":attendance_absent_list_student})


def add_staff(request):
    return render(request,'hod_templates/add_staff.html')


def save_staff(request):
    if request.method =="POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        address = request.POST.get("address")
        password = request.POST.get("password")
        try:
            user=CustomUser.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password,user_type=2)
            user.staffs.address = address
            user.save()
            messages.success(request,'Added Successfully')
            return HttpResponseRedirect('add_staff/')
        except:
            messages.error(request, 'Failed to add staff')
            return HttpResponseRedirect('add_staff/')

    else:
        return HttpResponse("Method not Allowed")


def manage_staff(request):
    staff=Staffs.objects.all()
    return render(request,'hod_templates/manage_staff.html',{'staff':staff})


def add_courses(request):
    return render(request,'hod_templates/add_courses.html')

def save_courses(request):
    if request.method =="POST":
        courses=request.POST.get("course_name")
        try:
            course_model=Courses(course_name=courses)
            course_model.save()
            messages.success(request,'Course Successfully Added')
            return HttpResponseRedirect('add_courses/')
        except:
            messages.error(request,'Failed To Add Course')
            return HttpResponseRedirect('add_courses/')
    else:
        return HttpResponse('Method not Allowed')

def manage_course(request):
    course=Courses.objects.all()
    return render(request,'hod_templates/manage_course.html',{'course':course})

def manage_student(request):
    student=Students.objects.all()
    return render(request,'hod_templates/manage_student.html',{"student":student})

def manage_subject(request):
    subject = Subjects.objects.all()
    return render(request,'hod_templates/manage_subject.html',{'subject':subject})

def add_students(request):
    course=Courses.objects.all()
    session=SessionYearModel.objects.all()
    return render(request,'hod_templates/add_students.html',{"courses":course,'session':session})



def save_students(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        address = request.POST.get("address")
        password = request.POST.get("password")
        session_id=request.POST.get('session_id')
        gender=request.POST.get("sex")
        course_id=request.POST.get("course_id")
        myfile = request.FILES.get('myfile',False)
        try:
            user = CustomUser.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                  email=email, password=password, user_type=3)
            user.students.address = address
            user.students.gender = gender
            course_obj=Courses.objects.get(id=course_id)
            user.students.courese_id = course_obj
            session=SessionYearModel.objects.get(id=session_id)
            user.students.session_year_id=session
            if myfile != False:
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
                user.students.profile_pic=uploaded_file_url
            user.save()
            messages.success(request, 'Added Successfully')
            return HttpResponseRedirect('add_students/')
        except:
             messages.error(request, 'Failed to add students')
             return HttpResponseRedirect('add_students')
    else:
        messages.success(request, 'Added Successfully')
        return HttpResponseRedirect('add_students')



def add_subjects(request):
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,'hod_templates/add_subjects.html',{"staffs":staffs,'courses':courses})

def save_subjects(request):
    if request.method =="POST":
        subject_name=request.POST.get('sub_name')
        course_id=request.POST.get('course_id')
        course=Courses.objects.get(id=course_id)
        staff_id=request.POST.get("staff_id")
        staff=CustomUser.objects.get(id=staff_id)
        try:
            subject=Subjects(subject=subject_name,course_id=course,stuff_id=staff)
            subject.save()
            messages.success(request, 'Successfully Added Subject')
            return HttpResponseRedirect('add_subjects/')
        except:
            messages.error(request, 'Failed to add Subject')
            return HttpResponseRedirect('add_subjects/')

    else:
        return HttpResponse("<h2>Method Not Allowed<h2>")

def edit_staff(request,staff_id):
    staff=Staffs.objects.get(admin = staff_id)
    return render(request,'hod_templates/edit_staff.html',{'staff':staff})


def save_edit_staff(request):
    if request.method =="POST":
        staff_id=request.POST.get("staff_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        address = request.POST.get("address")
        try:
            user = CustomUser.objects.get(id = staff_id)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            staff_model = Staffs.objects.get(admin = staff_id)
            staff_model.address = address
            staff_model.save()
            messages.success(request, 'Successfully Edit staff details')
            return HttpResponseRedirect('edit_staff/'+staff_id)
        except:
            messages.error(request, 'Failed to edit staff details')
            return HttpResponseRedirect("edit_staff/"+staff_id)


    else:
        return HttpResponse('<h2> Method NOt Allowed</h2>')

def edit_course(request,course_id):
    course=Courses.objects.get(id=course_id)
    return render(request,'hod_templates/edit_course.html',{'course':course})

def save_edit_course(request):
    if request.method=="POST":
        course_id= request.POST.get('course_id')
        courses_name=request.POST.get('course_name')
        try:
            course=Courses.objects.get(id=course_id)
            course.course_name=courses_name
            course.save()
            messages.success(request, 'Successfully Edit course details')
            return HttpResponseRedirect('edit_course/'+course_id)
        except:
            messages.error(request, 'Failed to edit staff details')
            return HttpResponseRedirect("edit_course/"+course_id)
    else:
        HttpResponse('Method Not Allowed')

def edit_student(request,student_id):
    student=Students.objects.get(admin=student_id)
    course=Courses.objects.all()
    session=SessionYearModel.objects.all()
    return render(request,'hod_templates/edit_student.html',{'student':student,'course':course,'session':session})

def save_edit_student(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        gender=request.POST.get('gender')
        address = request.POST.get("address")
        session_id=request.POST.get('session_id')

        course_id=request.POST.get('course_id')
        myfile=request.FILES.get('myfile',False)

        try:
            user = CustomUser.objects.get(id=student_id)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            student_model = Students.objects.get(admin=student_id)
            student_model.address = address
            student_model.gender = gender
            student_model.session_year_id_id = session_id
            student_model.courese_id_id = course_id
            if myfile !=False:
                fs=FileSystemStorage()
                filename=fs.save(myfile.name,myfile)
                uploded_url=fs.url(filename)
                student_model.profile_pic=uploded_url
            student_model.save()
            messages.success(request, 'Successfully Edit student details')
            return HttpResponseRedirect('edit_student/' + student_id)
        except:
            messages.error(request, 'Failed to  Edit student details')
            return HttpResponseRedirect('edit_student/' + student_id)
    else:
        HttpResponse('<h2>Method Not Allowed<h2>')

def edit_subject(request,subject_id):
    subjects=Subjects.objects.get(id=subject_id)
    staff=Staffs.objects.all()
    course=Courses.objects.all()
    return render(request,'hod_templates/edit_subject.html',{'subjects':subjects,'course':course,'staff':staff})

def save_edit_subject(request):
    if request.method == "POST":
        subject_name = request.POST.get("subject_name")
        course_id = request.POST.get("course_id")
        staff_id = request.POST.get("staff_id")
        subject_id=request.POST.get("subject_id")

        try:
            user = Subjects.objects.get(id=subject_id)
            user.subject = subject_name
            user.course_id_id = course_id
            user.stuff_id_id = staff_id
            user.save()
            messages.success(request, 'Successfully Edit subject details')
            return HttpResponseRedirect('edit_subject/'+subject_id)
        except:
            messages.success(request, 'Failed to Edit subject details')
            return HttpResponseRedirect('edit_subject/'+subject_id)
    else:
        HttpResponse('<h2>Method Not Allowed<h2>')


def manage_session(request):
    return render(request,'hod_templates/manage_session.html')

def save_session(request):
    if request.method=="POST":
        session_start=request.POST.get('session_start')
        session_end=request.POST.get('session_end')
        try:
            session=SessionYearModel(session_start_year=session_start,session_end_year=session_end)
            session.save()
            messages.success(request, 'Successfully Save Session details')
            return HttpResponseRedirect('manage_session/')
        except:
            messages.success(request, 'Failed to Save Session details')
            return HttpResponseRedirect('manage_session/')



def hod_student_feedback(request):
    feedbacks=FeedbackStudent.objects.all()
    return render(request,'hod_templates/hod_student_feedback.html',{'feedbacks':feedbacks})

def save_hod_student_feedback(request,feedback_id):
    feed_id=FeedbackStudent.objects.get(id=feedback_id)
    if request.method=="POST":
        try:
            feedback_replay = request.POST.get("feedback_replay")
            feed_id.feedback_reply = feedback_replay
            feed_id.save()
            messages.success(request,"Successfully Replay")
            return HttpResponseRedirect('/hod_student_feedback')
        except:
            messages.error(request, 'Failed to Replay')
            return HttpResponseRedirect('/hod_student_feedback')
    else:
        return HttpResponse('<h2>method not Allowed<h2>')

def hod_staff_feedback(request):
    feedbacks=FeedbackStaffs.objects.all()
    return render(request,'hod_templates/hod_staff_feedback.html',{'feedbacks':feedbacks})

def save_hod_staff_feedback(request,feedback_id):
    feed_id=FeedbackStaffs.objects.get(id=feedback_id)
    if request.method=="POST":
        try:
            feedback_replay = request.POST.get("feedback_replay")
            feed_id.feedback_reply = feedback_replay
            feed_id.save()
            messages.success(request,"Successfully Replay")
            return HttpResponseRedirect('/hod_staff_feedback')
        except:
            messages.error(request, 'Failed to Replay')
            return HttpResponseRedirect('/hod_staff_feedback')
    else:
        return HttpResponse('<h2>method not Allowed<h2>')


def hod_student_leave(request):
    leaves=LeaveReportStudent.objects.all()
    return render(request,'hod_templates/hod_student_leave.html',{'leaves':leaves})


def student_approve_leave(request,leave_id):
    leave=LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect("/hod_student_leave")

def student_disapprove_leave(request,leave_id):
    leave=LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status=0
    leave.save()
    return HttpResponseRedirect("/hod_student_leave")

def hod_staff_leave(request):
    leaves=LeaveReportStaff.objects.all()
    return render(request,'hod_templates/hod_staff_leave.html',{'leaves':leaves})


def staff_approve_leave(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect("/hod_staff_leave")

def staff_disapprove_leave(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=0
    leave.save()
    return HttpResponseRedirect("/hod_staff_leave")
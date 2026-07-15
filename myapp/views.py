from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import *
@login_required
def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    if request.method == "POST":
        form = TeacherForm(
            request.POST,
            request.FILES,
            instance=teacher
        )

        if form.is_valid():
            teacher = form.save()

            messages.success(
                request,
                f"تم تعديل بيانات الأستاذ {teacher.name}."
            )

            return redirect("teacher_list")

    else:
        form = TeacherForm(instance=teacher)

    return render_form_page(
        request,
        form,
        "تعديل أستاذ",
        "تعديل بيانات الأستاذ والمؤهل والراتب والحالة الوظيفية.",
        "teacher_list",
    )
@login_required
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    if request.method == "POST":
        name = teacher.name
        teacher.delete()

        messages.success(
            request,
            f"تم حذف الأستاذ {name}."
        )

        return redirect("teacher_list")

    return render(
        request,
        "teacher_confirm_delete.html",
        {
            "teacher": teacher
        }
    )
from .forms import (
    AssessmentForm,
    AttendanceRecordForm,
    CourseForm,
    EnrollmentForm,
    GradeRecordForm,
    InvoiceForm,
    PaymentForm,
    RegisterForm,
    StudentForm,
    TeacherForm,
)
def person_detail(request, pk):

    person = get_object_or_404(Person, pk=pk)

    context = {
        "person": person
    }

    return render(
        request,
        "person_detail.html",
        context
    )



def person_update(request, pk):

    person = get_object_or_404(Person, pk=pk)

    if request.method == "POST":

        form = PersonForm(
            request.POST,
            instance=person
        )

        if form.is_valid():
            form.save()
            return redirect("person_list")

    else:

        form = PersonForm(
            instance=person
        )


    return render(
        request,
        "person_form.html",
        {
            "form": form,
            "title": "تعديل شخص"
        }
    )



def person_delete(request, pk):

    person = get_object_or_404(Person, pk=pk)


    if request.method == "POST":

        person.delete()

        return redirect("person_list")


    return render(
        request,
        "person_delete.html",
        {
            "person": person
        }
    )
from .models import (
    Assessment,
    AttendanceRecord,
    Course,
    Enrollment,
    GradeRecord,
    Invoice,
    Payment,
    SchoolClass,
    Student,
    Teacher,
)


def user_role(request):
    if not request.user.is_authenticated:
        return None
    profile = getattr(request.user, "profile", None)
    return profile.role if profile else "admin"


def scope_students(request, queryset):
    profile = getattr(request.user, "profile", None)
    if not profile:
        return queryset
    if profile.role == "guardian" and profile.guardian:
        return queryset.filter(guardian=profile.guardian)
    if profile.role == "teacher" and profile.teacher:
        return queryset.filter(
             Q(enrollments__course__teacher=profile.teacher)
        ).distinct()
    return queryset


def scope_courses(request, queryset):
    profile = getattr(request.user, "profile", None)
    if profile and profile.role == "teacher" and profile.teacher:
        return queryset.filter(teacher=profile.teacher)
    return queryset


def scope_invoices(request, queryset):
    profile = getattr(request.user, "profile", None)
    if profile and profile.role == "guardian" and profile.guardian:
        return queryset.filter(student__guardian=profile.guardian)
    return queryset


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تم إنشاء الحساب بنجاح. يمكنك الآن تسجيل الدخول.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "auth/register.html", {"form": form})


def render_form_page(request, form, title, subtitle, back_url, meta_note=None, extra_context=None):
    context = {
        "form": form,
        "title": title,
        "subtitle": subtitle,
        "back_url": back_url,
        "meta_note": meta_note,
    }

    if extra_context:
        context.update(extra_context)

    return render(
        request,
        "form_page.html",
        context,
    )
@login_required
def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    return render(
        request,
        "teacher_detail.html",
        {
            "teacher": teacher
        }
    )
@login_required
def guardian_create(request):
    if request.method == "POST":
        form = GuardianForm(request.POST)

        if form.is_valid():
            guardian = form.save()

            messages.success(
                request,
                f"تمت إضافة ولي الأمر {guardian.name} بنجاح."
            )

            return redirect("student_create")

    else:
        form = GuardianForm()

    return render_form_page(
        request,
        form,
        "إضافة ولي أمر جديد",
        "سجل بيانات ولي الأمر ومعلومات التواصل.",
        "student_create",
        "يمكنك ربط ولي الأمر بالطلاب بعد الحفظ.",
    )
@login_required
def dashboard(request):
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_courses = Course.objects.count()
    total_classes = SchoolClass.objects.count()
    total_assessments = Assessment.objects.count()

    invoices = Invoice.objects.all()
    total_invoices = invoices.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    total_discounts = invoices.aggregate(total=Sum("discount"))["total"] or Decimal("0.00")
    total_payments = Payment.objects.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    outstanding_balance = max(total_invoices - total_discounts - total_payments, Decimal("0.00"))

    students_by_level = Student.objects.values("level").annotate(count=Count("id")).order_by("level")
    
    recent_payments = Payment.objects.select_related("invoice", "invoice__student").order_by("-payment_date")[:5]
    recent_assessments = Assessment.objects.select_related("course").order_by("-due_date")[:5]
    recent_attendance = AttendanceRecord.objects.select_related("student", "course").order_by("-date")[:6]
    average_grade = GradeRecord.objects.aggregate(avg=Avg("score"))["avg"] or 0

    context = {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_courses": total_courses,
        "total_classes": total_classes,
        "total_assessments": total_assessments,
        "average_grade": round(average_grade, 2),
        "outstanding_balance": outstanding_balance,
        "students_by_level": students_by_level,
        # "recent_students": recent_students,
        "recent_payments": recent_payments,
        "recent_assessments": recent_assessments,
        "recent_attendance": recent_attendance,
        "today": timezone.localdate(),
    }
    return render(request, "index.html", context)

from django.db.models import Q
from django.core.paginator import Paginator
from .models import Person
def person_list(request):
    query = request.GET.get("q", "")
    status_filter = request.GET.get("typestatus", "")
    gender_filter = request.GET.get("gender", "")

    persons = Person.objects.select_related(
        "name",
        "address",
        "national_id"
    ).all()

    if query:
        persons = persons.filter(
            Q(name__first_name__icontains=query)
            | Q(name__second_name__icontains=query)
            | Q(name__third_name__icontains=query)
            | Q(name__forth_name__icontains=query)
            | Q(name__last_name__icontains=query)
            | Q(phone__icontains=query)
            | Q(email__icontains=query)
        )

    if status_filter:
        persons = persons.filter(
            status=status_filter
        )

    if gender_filter:
        persons = persons.filter(
            gender=gender_filter
        )

    page_obj = Paginator(persons, 12).get_page(
        request.GET.get("page")
    )
    person_count = persons.count()

    page_obj = Paginator(persons, 12).get_page(
        request.GET.get("page")
    )
    return render(
        request,
        "person_list.html",
        {
            "page_obj": page_obj,
            "query": query,
            "status_filter": status_filter,
            "gender_filter": gender_filter,
            "status_choices": Person.STATUS_CHOICES,
            "person_count": person_count,
        },
    )
from .models import Student, AcademicYear
@login_required
@permission_required("myapp.view_student", raise_exception=True)
def student_list(request):
    query = request.GET.get("q", "")
    status_filter = request.GET.get("status", "")
    level_filter = request.GET.get("level", "")
    year_filter = request.GET.get("year", "")
    hijri_year_filter = request.GET.get("hijri_year", "")

    students = scope_students(
        request,
        Student.objects.select_related("guardian", "academic_year").all(),
    )

    if query:
        students = students.filter(
            Q(name__icontains=query)
            | Q(student_id__icontains=query)
            | Q(email__icontains=query)
            | Q(phone__icontains=query)
        )

    if status_filter:
        students = students.filter(status=status_filter)

    if level_filter:
        students = students.filter(level=level_filter)

    if year_filter:
        students = students.filter(
            academic_year__name__icontains=year_filter
        )

    if hijri_year_filter:
        students = students.filter(
            academic_year__hijri_year=hijri_year_filter
        )

    academic_years = AcademicYear.objects.all()

    hijri_year_choices = AcademicYear.HIJRI_YEAR_CHOICES

    page_obj = Paginator(
        students,
        12
    ).get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "student_list.html",
        {
            "page_obj": page_obj,
            "query": query,
            "status_filter": status_filter,
            "level_filter": level_filter,
            "year_filter": year_filter,
            "hijri_year_filter": hijri_year_filter,
            "level_choices": Student.LEVEL_CHOICES,
            "status_choices": Student.STATUS_CHOICES,
            "academic_years": academic_years,
            "hijri_year_choices": hijri_year_choices,
        },
    )
@login_required
@permission_required("myapp.add_student", raise_exception=True)
def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(request, f"تمت إضافة الطالب {student.name} بنجاح.")
            return redirect("student_list")
    else:
        form = StudentForm()
    return render_form_page(
        request,
        form,
        "إضافة طالب جديد",
        "سجل بيانات الطالب الأكاديمية والشخصية وبيانات ولي الأمر والطوارئ.",
        "student_list",
        "رقم الطالب يُولد تلقائيًا بعد الحفظ بصيغة احترافية سنوية.",
    )
from .forms import *
def name_create(request):
    if request.method == "POST":
        form = NameForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "تمت إضافة الاسم بنجاح."
            )

            return redirect("person_create")

    else:
        form = NameForm()


    return render(
        request,
        "name_form.html",
        {
            "form": form
        }
    )



def address_create(request):
    if request.method == "POST":
        form = AddressForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "تمت إضافة العنوان بنجاح."
            )

            return redirect("person_create")

    else:
        form = AddressForm()


    return render(
        request,
        "address_form.html",
        {
            "form": form
        }
    )



def personal_id_create(request):
    if request.method == "POST":
        form = PersonalIDCardForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "تمت إضافة البطاقة الشخصية بنجاح."
            )

            return redirect("person_create")

    else:
        form = PersonalIDCardForm()


    return render(
        request,
        "personal_id_form.html",
        {
            "form": form
        }
    )
from .forms import PersonForm
def person_create(request):
    if request.method == "POST":
        form = PersonForm(request.POST)

        if form.is_valid():

            person = form.save()

            messages.success(
                request,
                f"تمت إضافة الشخص {person} بنجاح."
            )

            return redirect("person_list")

    else:
        form = PersonForm()


    return render(
        request,
        "person_form.html",
        {
            "form": form
        }
    )
def name_create(request):
    if request.method == "POST":
        form = NameForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("person_create")

    else:
        form = NameForm()

    return render(
        request,
        "name_form.html",
        {"form": form}
    )



def address_create(request):
    if request.method == "POST":
        form = AddressForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("person_create")

    else:
        form = AddressForm()

    return render(
        request,
        "address_form.html",
        {"form": form}
    )



def personal_id_create(request):
    if request.method == "POST":
        form = PersonalIDCardForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("person_create")

    else:
        form = PersonalIDCardForm()

    return render(
        request,
        "personal_id_form.html",
        {"form": form}
    )
@login_required
@permission_required("myapp.change_student", raise_exception=True)
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save()
            messages.success(request, f"تم تحديث بيانات {student.name}.")
            return redirect("student_detail", pk=student.pk)
    else:
        form = StudentForm(instance=student)
    return render_form_page(
        request,
        form,
        "تعديل بيانات الطالب",
        "حدّث بيانات الطالب الأكاديمية والاتصالية دون فقدان السجل السابق.",
        "student_list",
        f"رقم الطالب الحالي: {student.student_id}",
    )


@login_required
@permission_required("myapp.view_student", raise_exception=True)
def student_detail(request, pk):
    student = get_object_or_404(
        scope_students(
            request,
            Student.objects.select_related("guardian",  "academic_year"),
        ),
        pk=pk,
    )
    enrollments = student.enrollments.select_related("course", "course__teacher")
    grade_records = student.grade_records.select_related("assessment", "assessment__course")[:8]
    attendance_summary = student.attendance_records.values("status").annotate(count=Count("id"))
    all_invoices = student.invoices.prefetch_related("payments").order_by("due_date")
    invoices = all_invoices[:6]
    total_paid = sum(invoice.paid_amount for invoice in all_invoices)
    total_due = sum(invoice.balance_due for invoice in all_invoices)
    average_grade = grade_records.aggregate(avg=Avg("score"))["avg"] or 0

    return render(
        request,
        "student_detail.html",
        {
            "student": student,
            "enrollments": enrollments,
            "grade_records": grade_records,
            "attendance_summary": attendance_summary,
            "invoices": invoices,
            "total_paid": total_paid,
            "total_due": total_due,
            "average_grade": round(average_grade, 2),
        },
    )


@login_required
@permission_required("myapp.delete_student", raise_exception=True)
def student_delete(request, pk):
    student = get_object_or_404(scope_students(request, Student.objects.all()), pk=pk)
    if request.method == "POST":
        name = student.name
        student.delete()
        messages.success(request, f"تم حذف الطالب {name}.")
        return redirect("student_list")
    return render(request, "student_confirm_delete.html", {"student": student})
from django.db.models import Q, Count

@login_required
@permission_required("myapp.view_teacher", raise_exception=True)


def teacher_list(request):

    query = request.GET.get("q", "")
    teacher_type_filter = request.GET.get("teacher_type", "")
    qualification_filter = request.GET.get("qualification", "")
    status_filter = request.GET.get("status", "")

    teachers = Teacher.objects.select_related(
        "name",
        "name__name"
    ).annotate(
        course_count=Count("courses")
    )

    # البحث
    if query:
        teachers = teachers.filter(
            Q(name__name__first_name__icontains=query) |
            Q(name__name__second_name__icontains=query) |
            Q(name__name__third_name__icontains=query) |
            Q(name__name__forth_name__icontains=query) |
            Q(name__name__last_name__icontains=query) |
            Q(name__phone__icontains=query) |
            Q(name__email__icontains=query) |
            Q(phone__icontains=query) |
            Q(specialization__icontains=query)
        )

    # فلترة نوع المعلم
    if teacher_type_filter:
        teachers = teachers.filter(
            teacher_type=teacher_type_filter
        )

    # فلترة المؤهل
    if qualification_filter:
        teachers = teachers.filter(
            qualification=qualification_filter
        )

    # فلترة الحالة
    if status_filter:
        teachers = teachers.filter(
            status=status_filter
        )

    context = {
        "teachers": teachers,
        "query": query,

        "teacher_types": Teacher.TEACHER_TYPE_CHOICES,
        "qualifications": Teacher.QUALIFICATION_CHOICES,
        "status_choices": Teacher.STATUS_CHOICES,

        "teacher_type_filter": teacher_type_filter,
        "qualification_filter": qualification_filter,
        "status_filter": status_filter,
    }

    return render(request, "teacher_list.html", context)
@login_required
@permission_required("myapp.add_teacher", raise_exception=True)
def teacher_create(request):
    if request.method == "POST":
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = form.save()
            messages.success(request, f"تمت إضافة الأستاذ {teacher.name}.")
            return redirect("teacher_list")
    else:
        form = TeacherForm()
    return render_form_page(
        request,
        form,
        "إضافة أستاذ",
        "أنشئ ملفًا متكاملًا للأستاذ يشمل المؤهل والتخصص والراتب والحالة الوظيفية.",
        "teacher_list",
    )


@login_required
@permission_required("myapp.view_course", raise_exception=True)
def course_list(request):
    query = request.GET.get("q", "")
    courses = scope_courses(
        request,
        Course.objects.select_related("teacher",  "academic_year").annotate(
            enrolled_count=Count("enrollments"),
            assessment_count=Count("assessments"),
        ),
    )
    if query:
        courses = courses.filter(Q(name__icontains=query) | Q(code__icontains=query))

    total_hours = courses.aggregate(total=Sum("credit_hours"))["total"] or 0
    return render(
        request,
        "course_list.html",
        {
            "courses": courses,
            "query": query,
            "total_hours": total_hours,
        },
    )


@login_required
@permission_required("myapp.add_course", raise_exception=True)
def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, f"تمت إضافة المادة {course.name}.")
            return redirect("course_list")
    else:
        form = CourseForm()
    return render_form_page(
        request,
        form,
        "إضافة مادة",
        "اربِط المادة بالصف الدراسي والأستاذ والعام الدراسي مع قواعد النجاح والدرجات.",
        "course_list",
    )


@login_required
@permission_required("myapp.view_enrollment", raise_exception=True)
def enrollment_list(request):
    enrollments = Enrollment.objects.select_related("student", "course", "course__teacher")
    enrollments = enrollments.filter(student__in=scope_students(request, Student.objects.all()))
    stats = {
        "total_enrollments": enrollments.count(),
        "completed_enrollments": enrollments.filter(grade__isnull=False).count(),
        "active_enrollments": enrollments.filter(grade__isnull=True).count(),
        "average_grade": round(enrollments.filter(grade__isnull=False).aggregate(avg=Avg("grade"))["avg"] or 0, 2),
    }
    return render(request, "enrollment_list.html", {"enrollments": enrollments, **stats})


@login_required
@permission_required("myapp.add_enrollment", raise_exception=True)
def enrollment_create(request):
    if request.method == "POST":
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تسجيل الطالب في المادة بنجاح.")
            return redirect("enrollment_list")
    else:
        form = EnrollmentForm()
    return render_form_page(
        request,
        form,
        "تسجيل طالب في مادة",
        "سجل الطالب في المادة مع إمكانية إدخال الدرجة النهائية ونسبة الحضور.",
        "enrollment_list",
    )


@login_required
@permission_required("myapp.view_assessment", raise_exception=True)
def assessment_list(request):
    assessments = Assessment.objects.select_related("course", "course__teacher").annotate(
        grades_count=Count("grade_records")
    ).filter(course__in=scope_courses(request, Course.objects.all()))
    return render(request, "assessment_list.html", {"assessments": assessments})


@login_required
@permission_required("myapp.add_assessment", raise_exception=True)
def assessment_create(request):
    if request.method == "POST":
        form = AssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save()
            messages.success(request, f"تم إنشاء التقييم {assessment.title}.")
            return redirect("assessment_list")
    else:
        form = AssessmentForm()
    return render_form_page(
        request,
        form,
        "إضافة تقييم",
        "أنشئ اختبارات وواجبات ومشاريع مع الوزن النسبي وموعد التنفيذ.",
        "assessment_list",
    )


@login_required
@permission_required("myapp.view_graderecord", raise_exception=True)
def gradebook_list(request):
    course_filter = request.GET.get("course", "")
    student_filter = request.GET.get("student", "")

    records = GradeRecord.objects.select_related("student", "assessment", "assessment__course")
    records = records.filter(student__in=scope_students(request, Student.objects.all()))
    records = records.filter(assessment__course__in=scope_courses(request, Course.objects.all()))
    if course_filter:
        records = records.filter(assessment__course_id=course_filter)
    if student_filter:
        records = records.filter(student_id=student_filter)

    return render(
        request,
        "gradebook_list.html",
        {
            "records": records,
            "courses": Course.objects.all(),
            "students": Student.objects.all()[:100],
            "course_filter": course_filter,
            "student_filter": student_filter,
            "average_score": round(records.aggregate(avg=Avg("score"))["avg"] or 0, 2),
        },
    )


@login_required
@permission_required("myapp.add_graderecord", raise_exception=True)
def grade_record_create(request):
    if request.method == "POST":
        form = GradeRecordForm(request.POST)
        if form.is_valid():
            record = form.save()
            messages.success(request, f"تم رصد درجة الطالب {record.student.name}.")
            return redirect("gradebook_list")
    else:
        form = GradeRecordForm()
    return render_form_page(
        request,
        form,
        "رصد درجة",
        "سجل نتيجة التقييم لكل طالب مع ملاحظات الأستاذ وتاريخ الرصد.",
        "gradebook_list",
    )


@login_required
@permission_required("myapp.view_attendancerecord", raise_exception=True)
def attendance_list(request):
    records_queryset = AttendanceRecord.objects.select_related("student", "course").order_by("-date")
    records_queryset = records_queryset.filter(student__in=scope_students(request, Student.objects.all()))
    records = records_queryset[:150]
    return render(
        request,
        "attendance_list.html",
        {
            "records": records,
            "present_count": records_queryset.filter(status="present").count(),
            "late_count": records_queryset.filter(status="late").count(),
            "absent_count": records_queryset.filter(status="absent").count(),
        },
    )


@login_required
@permission_required("myapp.add_attendancerecord", raise_exception=True)
def attendance_create(request):
    if request.method == "POST":
        form = AttendanceRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تم حفظ سجل الحضور.")
            return redirect("attendance_list")
    else:
        form = AttendanceRecordForm()
    return render_form_page(
        request,
        form,
        "إضافة سجل حضور",
        "وثّق حضور الطالب أو غيابه أو تأخره لكل يوم وكل مادة عند الحاجة.",
        "attendance_list",
    )


@login_required
@permission_required("myapp.view_invoice", raise_exception=True)
def finance_dashboard(request):
    invoices = scope_invoices(
        request,
        Invoice.objects.select_related("student", "category", "academic_year").prefetch_related("payments"),
    )
    recent_payments = Payment.objects.select_related("invoice", "invoice__student").filter(invoice__in=invoices)[:8]
    total_billed = invoices.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    total_discount = invoices.aggregate(total=Sum("discount"))["total"] or Decimal("0.00")
    total_paid = Payment.objects.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    total_due = max(total_billed - total_discount - total_paid, Decimal("0.00"))

    return render(
        request,
        "finance_dashboard.html",
        {
            "invoices": invoices[:20],
            "recent_payments": recent_payments,
            "total_billed": total_billed,
            "total_discount": total_discount,
            "total_paid": total_paid,
            "total_due": total_due,
            "overdue_count": invoices.filter(status="overdue").count(),
        },
    )


@login_required
@permission_required("myapp.add_invoice", raise_exception=True)
def invoice_create(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()
            invoice.refresh_status()
            invoice.save(update_fields=["status"])
            messages.success(request, f"تم إنشاء الفاتورة {invoice.title}.")
            return redirect("finance_dashboard")
    else:
        form = InvoiceForm()
    return render_form_page(
        request,
        form,
        "إصدار فاتورة",
        "أضف الرسوم الدراسية أو رسوم النقل أو أي بند مالي مع الخصومات والاستحقاق.",
        "finance_dashboard",
        "يُولد رقم الفاتورة تلقائيًا بمجرد الحفظ.",
    )


@login_required
@permission_required("myapp.add_payment", raise_exception=True)
def payment_create(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تسجيل الدفعة بنجاح.")
            return redirect("finance_dashboard")
    else:
        form = PaymentForm()
    return render_form_page(
        request,
        form,
        "تسجيل دفعة",
        "سجل سداد الرسوم مع طريقة الدفع والمرجع المالي.",
        "finance_dashboard",
    )


@login_required
def get_student_stats(request):
    stats = {
        "total_students": Student.objects.count(),
        "students_by_gender": list(Student.objects.values("gender").annotate(count=Count("id"))),
        "students_by_level": list(Student.objects.values("level").annotate(count=Count("id"))),
        "teacher_count": Teacher.objects.count(),
        "pending_invoices": Invoice.objects.filter(status__in=["pending", "partial", "overdue"]).count(),
    }
    return JsonResponse(stats)


@login_required
@permission_required("myapp.view_graderecord", raise_exception=True)
def report_card(request, pk):
    student = get_object_or_404(scope_students(request, Student.objects.all()), pk=pk)
    records = GradeRecord.objects.select_related("assessment", "assessment__course").filter(student=student)
    invoices = scope_invoices(request, Invoice.objects.filter(student=student).prefetch_related("payments"))
    return render(
        request,
        "reports/report_card.html",
        {
            "student": student,
            "records": records,
            "average_score": round(records.aggregate(avg=Avg("score"))["avg"] or 0, 2),
            "invoice_balance": sum(invoice.balance_due for invoice in invoices),
        },
    )


@login_required
@permission_required("myapp.view_invoice", raise_exception=True)
def invoice_print(request, pk):
    invoice = get_object_or_404(scope_invoices(request, Invoice.objects.prefetch_related("payments")), pk=pk)
    return render(request, "reports/invoice_print.html", {"invoice": invoice})

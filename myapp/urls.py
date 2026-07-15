from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views
from .forms import LoginForm


urlpatterns = [
 path(
    "persons/create/",
    views.person_create,
    name="person_create"
),
path(
    "persons/<int:pk>/",
    views.person_detail,
    name="person_detail"
),

path(
    "persons/<int:pk>/edit/",
    views.person_update,
    name="person_update"
),

path(
    "persons/<int:pk>/delete/",
    views.person_delete,
    name="person_delete"
),
path(
    "guardians/create/",
    views.guardian_create,
    name="guardian_create",
),
path("teachers/<int:pk>/", views.teacher_detail, name="teacher_detail"),

path("teachers/<int:pk>/edit/", views.teacher_update, name="teacher_update"),

path("teachers/<int:pk>/delete/", views.teacher_delete, name="teacher_delete"),
    path("persons/", views.person_list, name="person_list"),
    path("persons/", views.person_list, name="person_list"),
    path("login/", LoginView.as_view(template_name="auth/login.html", authentication_form=LoginForm), name="login"),
    path("register/", views.register, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", views.dashboard, name="dashboard"),
    path("students/", views.student_list, name="student_list"),
    path("students/create/", views.student_create, name="student_create"),
    path("students/<int:pk>/", views.student_detail, name="student_detail"),
    path("students/<int:pk>/edit/", views.student_update, name="student_update"),
    path("students/<int:pk>/delete/", views.student_delete, name="student_delete"),
    path("teachers/", views.teacher_list, name="teacher_list"),
    path("teachers/create/", views.teacher_create, name="teacher_create"),
    path("courses/", views.course_list, name="course_list"),
    path("courses/create/", views.course_create, name="course_create"),
    path("enrollments/", views.enrollment_list, name="enrollment_list"),
    path("enrollments/create/", views.enrollment_create, name="enrollment_create"),
    path("assessments/", views.assessment_list, name="assessment_list"),
    path("assessments/create/", views.assessment_create, name="assessment_create"),
    path("gradebook/", views.gradebook_list, name="gradebook_list"),
    path("gradebook/create/", views.grade_record_create, name="grade_record_create"),
    path("attendance/", views.attendance_list, name="attendance_list"),
    path("attendance/create/", views.attendance_create, name="attendance_create"),
    path("finance/", views.finance_dashboard, name="finance_dashboard"),
    path("finance/invoices/create/", views.invoice_create, name="invoice_create"),
    path("finance/invoices/<int:pk>/print/", views.invoice_print, name="invoice_print"),
    path("finance/payments/create/", views.payment_create, name="payment_create"),
    path("students/<int:pk>/report-card/", views.report_card, name="report_card"),
    path("api/student-stats/", views.get_student_stats, name="student_stats"),
path("names/create/", views.name_create, name="name_create"),

path("addresses/create/", views.address_create, name="address_create"),

path("cards/create/", views.personal_id_create, name="personal_id_create"),
]

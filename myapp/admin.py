from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

@admin.register(Name)
class NameAdmin(ImportExportModelAdmin):
    list_display = (
        "first_name",
        "second_name",
        "third_name",
        "forth_name",
        "last_name",
        "arabic_full_name",
    )
    
    search_fields = (
        "first_name",
        "second_name",
        "third_name",
        "forth_name",
        "last_name",
        "arabic_full_name",
    )

    def has_module_permission(self, request):
        return False


# Admin for Address
@admin.register(Address)
class AddressAdmin(ImportExportModelAdmin):
    list_display = ("street", "city", "state", "country")
    search_fields = ("street", "city", "state", "country")

    def has_module_permission(self, request):
        return False
@admin.register(PersonalIDCard)
class PersonalIDCardAdmin(ImportExportModelAdmin):
    def has_module_permission(self, request):
        return False

    list_display = ("card_number", "issue_date", "expiry_date", "governorate")
    search_fields = ("person__name__first_name", "card_number")
    list_filter = ("issue_date", "expiry_date", "governorate")

    fieldsets = (
        ("معلومات البطاقة", {"fields": ("card_number", "issue_date", "expiry_date")}),
        (
            "مكان الميلاد",
            {"fields": ("governorate", "district", "sub_district", "village")},
        ),
        ("فصيلة الدم:", {"fields": ("blood_Type",)}),
    )
@admin.register(Person)
class PersonAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
     

        
    )

    list_display_links  = (
        "name",

    )

    search_fields = (
    "name__first_name",
    "name__second_name",
    "name__third_name",
    "name__forth_name",
    "name__last_name",
    "phone",
    )

    list_filter = [
        "address__city",
     
       "gender",
        "marital_status",
        "health_condition",
     
    ]

    autocomplete_fields = ["name", "address", "national_id"]

    actions = ["export_as_excel"]
    
    fieldsets = (
    (
        "المعلومات الشخصية",
        {
            "fields": (
                "name",
                "address",
                "date_of_birth",
                "gender",
                "marital_status",
                "national_id",
                
                "male_children",
                "female_children",
                "health_condition",
                "status",
            )
        },
        ),
        (
        "معلومات التواصل",
        {
            "fields": (
                "phone",
                "email",
            )
        },
        ),
           )
    (
            "معلومات التواصل",
            {
                "fields": (
                    "phone",
                    "email",
                )
            },
        ),
    
    
            
    (
            "التوقف",
            {
                "fields": (
                    
              
                    
                    "exit_date",
                    
                )
            },
        ),
      
    
    
     # داخل كلاس PersonAdmin
    def get_fieldsets(self, request, obj=None):
       restricted_users = ["abas", "sadiq", "mjad", "taloot"] 
       if request.user.username in restricted_users:
          return (
            ("المعلومات الشخصية", {"fields": ("name",)}),
          )
  
       return super().get_fieldsets(request, obj)


    def export_as_excel(self, request, queryset):
        import openpyxl
        from django.http import HttpResponse

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Persons"
        headers = [
            "الاسم",
            "رقم الجوال",
            "متواجد",
            "البريد الإلكتروني",
            "العنوان",
            "تاريخ الميلاد",
            "رقم البطاقة",
            "المؤهل العلمي",
            "معدل الثانوية العامة",
            "تأريخ الدخول",
          
            "الحالة المادية",
            "الحالة الأجتماعية",
       
        ]
        ws.append(headers)
        for obj in queryset:
            ws.append(
                [
                    str(obj.name),
                    obj.phone,
                  
                  
                    obj.email,
                    str(obj.address),
                    obj.date_of_birth,
                    str(obj.national_id),
                    
     
                   
     
                    obj.status,
                    obj.marital_status,
                    obj.health_condition,
               
                ]
            )

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = "attachment; filename=persons.xlsx"
        wb.save(response)
        return response
    def delete_link(self, obj):
        from django.utils.html import format_html
        return format_html('<a href="/admin/HR/person/{}/delete/">ازاله</a>', obj.id)
    
    delete_link.short_description = "حذف"

    export_as_excel.short_description = "تصدير إلى Excel"

from .models import (
    AcademicYear,
    Assessment,
    AttendanceRecord,
    Course,
    Enrollment,
    FeeCategory,
    GradeRecord,
    Guardian,
    Invoice,
    Payment,
    SchoolClass,
    Student,
    Teacher,
    UserProfile,
)


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "end_date", "is_current"]
    list_filter = ["is_current"]
    search_fields = ["name"]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = [ "name", "status", "hire_date", "salary"]
    list_filter = ["status"]
    search_fields = [ "name", "phone", "email"]


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ["name", "academic_year", "stage", "level", "section", "capacity", "homeroom_teacher"]
    list_filter = ["academic_year", "stage", "level"]
    search_fields = ["name", "section", "room_number"]


@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = ["name", "relationship", "phone", "email"]
    list_filter = ["relationship"]
    search_fields = ["name", "phone", "email"]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["student_id", "name", "level", "status", "guardian", "created_at"]
    list_filter = ["level", "status",  "academic_year"]
    search_fields = ["student_id", "name", "phone", "email"]
    autocomplete_fields = ["guardian",  "academic_year"]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "level", "teacher",  "course_type", "credit_hours"]
    list_filter = ["level", "course_type", "academic_year"]
    search_fields = ["code", "name"]
    autocomplete_fields = ["teacher",  "academic_year"]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ["student", "course", "grade", "attendance_percentage", "enrollment_date"]
    list_filter = ["course", "enrollment_date"]
    search_fields = ["student__name", "course__name"]
    autocomplete_fields = ["student", "course"]


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ["student", "course", "date", "status"]
    list_filter = ["status", "date", "course"]
    search_fields = ["student__name", "course__name"]
    autocomplete_fields = ["student", "course"]


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ["title", "course", "assessment_type", "term", "max_score", "weight", "due_date"]
    list_filter = ["assessment_type", "term", "course"]
    search_fields = ["title", "course__name"]
    autocomplete_fields = ["course"]


@admin.register(GradeRecord)
class GradeRecordAdmin(admin.ModelAdmin):
    list_display = ["student", "assessment", "score", "graded_at"]
    list_filter = ["graded_at", "assessment__course"]
    search_fields = ["student__name", "assessment__title", "assessment__course__name"]
    autocomplete_fields = ["student", "assessment"]


@admin.register(FeeCategory)
class FeeCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "default_amount"]
    search_fields = ["name"]


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["title", "student", "category", "amount", "discount", "status", "due_date"]
    list_filter = ["status", "category", "academic_year"]
    search_fields = ["title", "student__name", "student__student_id"]
    autocomplete_fields = ["student", "academic_year", "category"]
    inlines = [PaymentInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["invoice", "amount", "payment_date", "method"]
    list_filter = ["method", "payment_date"]
    search_fields = ["invoice__title", "invoice__student__name", "reference_number"]
    autocomplete_fields = ["invoice"]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "role", "teacher", "guardian", "student"]
    list_filter = ["role"]
    search_fields = ["user__username", "user__email"]
    autocomplete_fields = ["user", "teacher", "guardian", "student"]

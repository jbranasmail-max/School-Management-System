from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django_select2.forms import Select2Widget
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
)


class StyledModelForm(forms.ModelForm):
    date_fields = {"DateInput": {"type": "date"}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            classes = "form-control"
            if isinstance(widget, forms.CheckboxInput):
                classes = "form-check-input"
            elif isinstance(widget, forms.FileInput):
                classes = "form-control form-control-file"
            widget.attrs["class"] = f"{widget.attrs.get('class', '').strip()} {classes}".strip()
            if isinstance(widget, forms.DateInput):
                widget.input_type = "date"


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="اسم المستخدم")
    password = forms.CharField(label="كلمة المرور", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="اسم المستخدم")
    email = forms.EmailField(label="البريد الإلكتروني", required=False)
    password1 = forms.CharField(label="كلمة المرور", widget=forms.PasswordInput)
    password2 = forms.CharField(label="تأكيد كلمة المرور", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

class TeacherForm(StyledModelForm):
    class Meta:
        model = Teacher
        fields = [
            "name",
            "specialization",
            "qualification",
            "hire_date",
            "salary",
            "status",
            "photo",
            "experience_years",
            "teacher_type",
            "address",
            "notes",
        ]

        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
class GuardianForm(StyledModelForm):
    class Meta:
        model = Guardian
        fields = [
            "name",
            "relationship",
            "phone",
            "alternate_phone",
            "email",
            "occupation",
            "address",
        ]
        widgets = {"address": forms.Textarea(attrs={"rows": 3})}


class SchoolClassForm(StyledModelForm):
    class Meta:
        model = SchoolClass
        fields = [
            "academic_year",
            "name",
            "stage",
            "level",
            "section",
            "room_number",
            "capacity",
            "homeroom_teacher",
        ]

class StudentForm(StyledModelForm):

    class Meta:
        model = Student
        fields = [
            "name",
            "level",
            "semester",
            "academic_year",
          
            "guardian",
            "admission_date",
            "status",
            "address",
            
            "emergency_contact_name",
            "hijri_year",
            "emergency_contact_phone",
            "photo",
            "notes",
        ]

        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].help_text = (
            "يولّد رقم الطالب تلقائيًا عند الحفظ لأول مرة."
        )

        self.fields["academic_year"].queryset = AcademicYear.objects.all().order_by("-start_date")

        self.fields["academic_year"].label_from_instance = (
        lambda obj: f"{obj.name} - {obj.hijri_year} هـ"
        if obj.hijri_year
        else obj.name
        )
        
        self.fields["guardian"].queryset = Guardian.objects.all()


        # عرض الأعوام الدراسية مرتبة من الأحدث إلى الأقدم
        self.fields["academic_year"].label = "العام الدراسي (ميلادي / هجري)"

        self.fields["academic_year"].choices = [
            (
                year.id,
                f"{year.name} - {year.hijri_year} هـ"
                if year.hijri_year
                else year.name
            )
            for year in AcademicYear.objects.all().order_by("-start_date")
        ]
from .models import Person, Name, Address, PersonalIDCard
class PersonForm(StyledModelForm):

    class Meta:
        model = Person

        fields = [
            "name",
            "address",
            "date_of_birth",
            "national_id",
            "phone",
            "email",

            "gender",

            "status",
          
            "marital_status",

            "male_children",
            "female_children",

            "health_condition",
        ]

        widgets = {

            "name": Select2Widget(
                attrs={
                    "data-placeholder": "ابحث عن الاسم..."
                }
            ),


            "address": Select2Widget(
                attrs={
                    "data-placeholder": "ابحث عن العنوان..."
                }
            ),


            "national_id": Select2Widget(
                attrs={
                    "data-placeholder": "ابحث عن البطاقة..."
                }
            ),


            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

        }
class NameForm(StyledModelForm):
    class Meta:
        model = Name
        fields = [
            "first_name",
            "second_name",
            "third_name",
            "forth_name",
            "last_name",
        ]


class AddressForm(StyledModelForm):
    class Meta:
        model = Address
        fields = [
            "street",
            "city",
            "state",
            "country",
        ]


class PersonalIDCardForm(StyledModelForm):
    class Meta:
        model = PersonalIDCard
        fields = [
            "card_number",
            "issue_date",
            "expiry_date",
            "governorate",
            "district",
            "sub_district",
            "village",
            "blood_Type",
        ]
class CourseForm(StyledModelForm):
    class Meta:
        model = Course
        fields = [
            "code",
            "name",
            "description",
            "credit_hours",
            "level",
            "course_type",
            "academic_year",
            
            "teacher",
            "pass_mark",
            "max_marks",
        ]
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}


class EnrollmentForm(StyledModelForm):
    class Meta:
        model = Enrollment
        fields = ["student", "course", "grade", "attendance_percentage"]
        widgets = {
            "grade": forms.NumberInput(attrs={"min": 0, "max": 100, "step": 0.01}),
            "attendance_percentage": forms.NumberInput(
                attrs={"min": 0, "max": 100, "step": 0.01}
            ),
        }


class AttendanceRecordForm(StyledModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ["student", "course", "date", "status", "notes"]


class AssessmentForm(StyledModelForm):
    class Meta:
        model = Assessment
        fields = [
            "course",
            "title",
            "assessment_type",
            "term",
            "max_score",
            "weight",
            "due_date",
            "instructions",
        ]
        widgets = {"instructions": forms.Textarea(attrs={"rows": 4})}


class GradeRecordForm(StyledModelForm):
    class Meta:
        model = GradeRecord
        fields = ["student", "assessment", "score", "feedback", "graded_at"]
        widgets = {"feedback": forms.Textarea(attrs={"rows": 3})}


class FeeCategoryForm(StyledModelForm):
    class Meta:
        model = FeeCategory
        fields = ["name", "description", "default_amount"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}


class InvoiceForm(StyledModelForm):
    class Meta:
        model = Invoice
        fields = [
            "student",
            "academic_year",
            "category",
            "title",
            "amount",
            "discount",
            "due_date",
            "status",
            "notes",
        ]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}


class PaymentForm(StyledModelForm):
    class Meta:
        model = Payment
        fields = ["invoice", "amount", "payment_date", "method", "reference_number", "notes"]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}

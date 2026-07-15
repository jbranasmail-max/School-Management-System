from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg, Sum
from django.utils import timezone
class Name(models.Model):
    def __str__(self):
        return f"{self.first_name} {self.second_name or ''} {self.third_name} {self.forth_name} {self.last_name} ".strip()
    first_name = models.CharField("الاسم الأول", max_length=100)
    second_name = models.CharField("اسم الأب", max_length=100, blank=True, null=True)
    third_name = models.CharField("اسم الثالث", max_length=100, blank=True, null=True)
    forth_name = models.CharField("اسم الرابع", max_length=100, blank=True, null=True)
    last_name = models.CharField("اسم العائلة", max_length=100)
    
    @property
    def arabic_full_name(self):
        parts = [
            self.first_name,
            self.second_name,
            self.third_name,
            self.forth_name,
            self.last_name,
        ]
        return " ".join([p for p in parts if p]).strip()

    class Meta:
        verbose_name = "الاسم الكامل"
        verbose_name_plural = "الأسماء الكاملة"
# العناوين
class Address(models.Model):
    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}"
# الترتيب: city (المديرية) ← street (المحافظة) ← state ← country
    street = models.CharField("المحافظة", max_length=255)
    city = models.CharField("المديرية", max_length=100)
    state = models.CharField("العزلة", max_length=100)
    country = models.CharField("القرية", max_length=100)

    class Meta:
        verbose_name = "العنوان"
        verbose_name_plural = "العناوين"


# البطاقات الشخصية
class PersonalIDCard(models.Model):
    def __str__(self):
        return f"{self.card_number}"
    card_number = models.CharField("رقم البطاقة", max_length=50)
    issue_date = models.DateField("تاريخ الإصدار")
    expiry_date = models.DateField("تاريخ الانتهاء")
    governorate = models.CharField("المحافظة", max_length=50, blank=True, null=True)
    district = models.CharField("المديرية", max_length=50, blank=True, null=True)
    sub_district = models.CharField("العزلة", max_length=50, blank=True, null=True)
    village = models.CharField("القرية", max_length=50, blank=True, null=True)
    BLOOD_TYPES_CHOICES = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    ]
    blood_Type = models.CharField(
        "فصيلة الدم", choices=BLOOD_TYPES_CHOICES, max_length=10, null=True
    )

    class Meta:
        verbose_name = "بطاقة الهوية الشخصية"
        verbose_name_plural = "بطاقات الهوية الشخصية"

# الاشخاص
from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models



class Person(models.Model):
    MARITAL_STATUS_CHOICES = [
    ("أعزب", "أعزب"),
    ("متزوج", "متزوج"),
    ]

    HEALTH_CONDITION_CHOICES = [
    ("جيد", "جيد"),
    ("متوسط", "متوسط"),
    ("سيئ", "سيئ"),
    ("ذو إعاقة", "ذو إعاقة"),
    ("مريض مزمن", "مريض مزمن"),
    ]

    STATUS_CHOICES = [
    ("جيد", "جيد"),
    ("متوسط", "متوسط"),
    ("ضعيف", "ضعيف"),
    ("فقير جدًا", "فقير جدًا"),
    ("يتيم", "يتيم"),
    ]
    @property
    def no_violation_for_six_months(self):
        from datetime import date, timedelta

        six_months_ago = date.today() - timedelta(days=180)
        return not self.violation_set.filter(date__gte=six_months_ago).exists()


    def __str__(self):
        return str(self.name)


    # الحقول الأساسية
    name = models.OneToOneField(
        Name,
        on_delete=models.CASCADE,
        verbose_name="الاسم"
    )


    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="العنوان"
    )
    GENDER_CHOICES = [
        ("M", "ذكر"),
        ("F", "أنثى"),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="الجنس")
   
    date_of_birth = models.DateField(
        "تاريخ الميلاد",
        blank=True,
        null=True
    )

    national_id = models.OneToOneField(
        PersonalIDCard,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="person",
        verbose_name="البطاقة الشخصية",
    )

    phone = models.CharField(
        "رقم الجوال",
        max_length=100,
        blank=True,
        null=True
    )
    email = models.EmailField(
    "البريد الإلكتروني",
    max_length=255,
    blank=True,
    null=True
    )
    

    # الحالة الاجتماعية
    marital_status = models.CharField(
        "الحالة الاجتماعية",
        choices=MARITAL_STATUS_CHOICES,
        max_length=50,
        blank=True,
        null=True
    )


    male_children = models.PositiveIntegerField(
        "عدد الأولاد الذكور",
        blank=True,
        null=True,
        default=0
    )

    female_children = models.PositiveIntegerField(
        "عدد الأولاد الإناث",
        blank=True,
        null=True,
        default=0
    )


    total_children = models.PositiveIntegerField(
        "إجمالي الأولاد",
        editable=False,
        blank=True,
        null=True,
        default=0
    )


    # الحالة الصحية
    health_condition = models.CharField(
        "الحالة الصحية",
        choices=HEALTH_CONDITION_CHOICES,
        max_length=255,
        blank=True,
        null=True
    )


    # الحالة المادية والاجتماعية
    status = models.CharField(
        "الحالة المادية",
        choices=STATUS_CHOICES,
        max_length=100,
        blank=True,
        null=True
    )


    def save(self, *args, **kwargs):
        self.total_children = (
            (self.male_children or 0)
            +
            (self.female_children or 0)
        )

        super().save(*args, **kwargs)



    class Meta:
        verbose_name = "اسم"
        verbose_name_plural = "الاسماء"

def build_sequential_code(model, field_name, prefix, width=4):
    existing = set(
        model.objects.filter(**{f"{field_name}__startswith": prefix}).values_list(field_name, flat=True)
    )
    sequence = 1
    while f"{prefix}{sequence:0{width}d}" in existing:
        sequence += 1
    return f"{prefix}{sequence:0{width}d}"

class AcademicYear(models.Model):

    name = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="العام الدراسي"
    )

    start_date = models.DateField(
        verbose_name="تاريخ البداية"
    )

    end_date = models.DateField(
        verbose_name="تاريخ النهاية"
    )

    HIJRI_YEAR_CHOICES = [
        (year, f"{year} هـ")
        for year in range(1435, 1466)
    ]

    hijri_year = models.PositiveIntegerField(
        choices=HIJRI_YEAR_CHOICES,
        verbose_name="السنة الهجرية",
        null=True,
        blank=True
    )

    is_current = models.BooleanField(
        default=False,
        verbose_name="العام الحالي"
    )


    class Meta:
        verbose_name = "عام دراسي"
        verbose_name_plural = "الأعوام الدراسية"
        ordering = ["-start_date"]


    def __str__(self):
        if self.hijri_year:
            return f"{self.name} / {self.hijri_year} هـ"

        return self.name

@classmethod
def create_default_years(cls):
    years = []

    hijri_start = 1435

    for year in range(2020, 2051):
        name = f"{year}-{year + 1}"
        hijri_year = hijri_start + (year - 2020)

        obj, created = cls.objects.get_or_create(
            name=name,
            defaults={
                "start_date": f"{year}-09-01",
                "end_date": f"{year + 1}-06-30",
                "hijri_year": hijri_year,
                "is_current": False,
            }
        )

        if created:
            years.append(obj)

    return years
class Teacher(models.Model):

    STATUS_CHOICES = [
        ("active", "على رأس العمل"),
        ("leave", "إجازة"),
        ("inactive", "غير نشط"),
    ]

    QUALIFICATION_CHOICES = [
        ("ثانوي", "ثانوي"),
        ("دبلوم", "دبلوم"),
        ("بكالوريوس", "بكالوريوس"),
        ("ماجستير", "ماجستير"),
        ("دكتوراه", "دكتوراه"),
        ("أخرى", "أخرى"),
    ]

    TEACHER_TYPE_CHOICES = [
        ("fixed", "ثابت"),
        ("volunteer", "متطوع"),
        ("contract", "متعاقد"),
        ("temporary", "مؤقت"),
        ("part_time", "دوام جزئي"),
        ("substitute", "بديل"),
        ("trainee", "متدرب"),
    ]

    name = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        verbose_name="الشخص"
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="رقم الهاتف"
    )

    specialization = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="التخصص"
    )

    teacher_type = models.CharField(
        max_length=20,
        choices=TEACHER_TYPE_CHOICES,
        default="fixed",
        verbose_name="نوع المعلم"
    )

    qualification = models.CharField(
        max_length=20,
        choices=QUALIFICATION_CHOICES,
        blank=True,
        verbose_name="المؤهل"
    )

    experience_years = models.PositiveIntegerField(
        default=0,
        verbose_name="سنين الخبرة"
    )

    hire_date = models.DateField(
        default=timezone.localdate,
        verbose_name="تاريخ التعيين"
    )

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="الراتب الأساسي"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="active",
        verbose_name="الحالة الوظيفية"
    )

    photo = models.ImageField(
        upload_to="teachers/photos/",
        null=True,
        blank=True,
        verbose_name="الصورة"
    )

    address = models.TextField(
        blank=True,
        verbose_name="العنوان"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="ملاحظات"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإضافة"
    )


    class Meta:
        verbose_name = "أستاذ"
        verbose_name_plural = "الأساتذة"
        ordering = ["name"]


    def __str__(self):
        return str(self.name)
class SchoolClass(models.Model):
    STAGE_CHOICES = [
        ("primary", "ابتدائي"),
        ("middle", "إعدادي"),
        ("secondary", "ثانوي"),
    ]

    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        related_name="classes",
        verbose_name="العام الدراسي",
    )
    name = models.CharField(max_length=80, verbose_name="اسم الصف/الشعبة")
    stage = models.CharField(max_length=10, choices=STAGE_CHOICES, verbose_name="المرحلة")
    level = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name="الصف",
    )
    section = models.CharField(max_length=20, blank=True, verbose_name="الشعبة")
    room_number = models.CharField(max_length=20, blank=True, verbose_name="القاعة")
    capacity = models.PositiveIntegerField(default=30, verbose_name="السعة")
    homeroom_teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="homeroom_classes",
        verbose_name="المربي/المرشدة",
    )

    class Meta:
        verbose_name = "صف دراسي"
        verbose_name_plural = "الصفوف الدراسية"
        ordering = ["academic_year__start_date", "level", "section", "name"]
        unique_together = ["academic_year", "name"]

    def __str__(self):
        return f"{self.name} - {self.academic_year.name}"


class Guardian(models.Model):
    RELATION_CHOICES = [
        ("father", "الأب"),
        ("mother", "الأم"),
        ("brother", "الأخ"),
        ("sister", "الأخت"),
        ("other", "قريب آخر"),
    ]

    name = models.CharField(max_length=120, verbose_name="اسم ولي الأمر")
    relationship = models.CharField(
        max_length=10,
        choices=RELATION_CHOICES,
        default="father",
        verbose_name="صلة القرابة",
    )
    phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    alternate_phone = models.CharField(max_length=20, blank=True, verbose_name="رقم إضافي")
    email = models.EmailField(blank=True, verbose_name="البريد الإلكتروني")
    occupation = models.CharField(max_length=120, blank=True, verbose_name="الوظيفة")
    address = models.TextField(blank=True, verbose_name="العنوان")

    class Meta:
        verbose_name = "ولي أمر"
        verbose_name_plural = "أولياء الأمور"
        ordering = ["name"]

    def __str__(self):
        return self.name
class Student(models.Model):

    STATUS_CHOICES = [
        ("active", "نشط"),
        ("suspended", "موقوف"),
        ("graduated", "متخرج"),
        ("withdrawn", "منسحب"),
    ]


    LEVEL_CHOICES = [
        ("تمهيدي", "تمهيدي"),

        ("الأول ابتدائي", "الأول ابتدائي"),
        ("الثاني ابتدائي", "الثاني ابتدائي"),
        ("الثالث ابتدائي", "الثالث ابتدائي"),
        ("الرابع ابتدائي", "الرابع ابتدائي"),
        ("الخامس ابتدائي", "الخامس ابتدائي"),
        ("السادس ابتدائي", "السادس ابتدائي"),

        ("الأول متوسط", "الأول متوسط"),
        ("الثاني متوسط", "الثاني متوسط"),
        ("الثالث متوسط", "الثالث متوسط"),

        ("الأول ثانوي علمي", "الأول ثانوي علمي"),
        ("الثاني ثانوي علمي", "الثاني ثانوي علمي"),
        ("الثالث ثانوي علمي", "الثالث ثانوي علمي"),

        ("الأول ثانوي أدبي", "الأول ثانوي أدبي"),
        ("الثاني ثانوي أدبي", "الثاني ثانوي أدبي"),
        ("الثالث ثانوي أدبي", "الثالث ثانوي أدبي"),
    ]


    SEMESTER_CHOICES = [
        ("first", "الأول"),
        ("second", "الثاني"),
        ("all", "الكل"),
    ]


    student_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        editable=False,
        verbose_name="رقم الطالب",
    )


    name = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        verbose_name="الشخص"
    )


    level = models.CharField(
        max_length=50,
        choices=LEVEL_CHOICES,
        verbose_name="الصف"
    )


    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
        verbose_name="العام الدراسي",
    )
    HIJRI_YEAR_CHOICES = [
    (year, f"{year} هـ")
    for year in range(1435, 1466)
    ]

    hijri_year = models.PositiveIntegerField(
    choices=HIJRI_YEAR_CHOICES,
    verbose_name="السنة الهجرية",
    null=True,
    blank=True
   )


    semester = models.CharField(
        max_length=10,
        choices=SEMESTER_CHOICES,
        default="all",
        verbose_name="الفصل الدراسي",
    )


    


    guardian = models.ForeignKey(
        Guardian,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
        verbose_name="ولي الأمر",
    )


    admission_date = models.DateField(
        default=timezone.localdate,
        verbose_name="تاريخ القبول"
    )


    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default="active",
        verbose_name="الحالة الدراسية",
    )


    address = models.TextField(
        blank=True,
        verbose_name="العنوان"
    )


    emergency_contact_name = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="اسم جهة الطوارئ",
    )


    emergency_contact_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="هاتف الطوارئ",
    )


    photo = models.ImageField(
        upload_to="students/photos/",
        null=True,
        blank=True,
        verbose_name="صورة الطالب",
    )


    notes = models.TextField(
        blank=True,
        verbose_name="ملاحظات"
    )


    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإضافة"
    )


    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاريخ التحديث"
    )


    class Meta:
        verbose_name = "طالب"
        verbose_name_plural = "الطلاب"
        ordering = ["-created_at"]


    def __str__(self):
        return f"{self.name} ({self.student_id})"


    @property
    def average_score(self):
        value = self.grade_records.aggregate(avg=Avg("score"))["avg"]
        return value or Decimal("0.00")


    def save(self, *args, **kwargs):

        if not self.student_id:

            year_seed = (
                self.academic_year.start_date.year
                if self.academic_year and self.academic_year.start_date
                else timezone.localdate().year
            )


            prefix = f"STU-{year_seed}-"


            self.student_id = build_sequential_code(
                Student,
                "student_id",
                prefix
            )


        super().save(*args, **kwargs)
class Course(models.Model):
    COURSE_TYPE_CHOICES = [
        ("core", "أساسية"),
        ("lab", "عملي"),
        ("activity", "نشاط"),
        ("elective", "اختيارية"),
    ]
    LEVEL_CHOICES = [
        ("تمهيدي", "تمهيدي"),

        ("الأول ابتدائي", "الأول ابتدائي"),
        ("الثاني ابتدائي", "الثاني ابتدائي"),
        ("الثالث ابتدائي", "الثالث ابتدائي"),
        ("الرابع ابتدائي", "الرابع ابتدائي"),
        ("الخامس ابتدائي", "الخامس ابتدائي"),
        ("السادس ابتدائي", "السادس ابتدائي"),

        ("الأول متوسط", "الأول متوسط"),
        ("الثاني متوسط", "الثاني متوسط"),
        ("الثالث متوسط", "الثالث متوسط"),

        ("الأول ثانوي علمي", "الأول ثانوي علمي"),
        ("الثاني ثانوي علمي", "الثاني ثانوي علمي"),
        ("الثالث ثانوي علمي", "الثالث ثانوي علمي"),

        ("الأول ثانوي أدبي", "الأول ثانوي أدبي"),
        ("الثاني ثانوي أدبي", "الثاني ثانوي أدبي"),
        ("الثالث ثانوي أدبي", "الثالث ثانوي أدبي"),
    ]

    code = models.CharField(max_length=10, unique=True, verbose_name="رمز المادة")
    name = models.CharField(max_length=100, verbose_name="اسم المادة")
    description = models.TextField(blank=True, verbose_name="وصف المادة")
    credit_hours = models.IntegerField(default=1, verbose_name="عدد الحصص/الساعات")
    level = models.CharField(
    max_length=50,
    choices=LEVEL_CHOICES,
    verbose_name="الصف"
    )
    course_type = models.CharField(
        max_length=10,
        choices=COURSE_TYPE_CHOICES,
        default="core",
        verbose_name="نوع المادة",
    )
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
        verbose_name="العام الدراسي",
    )
    
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
        verbose_name="الأستاذ المسؤول",
    )
    pass_mark = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="درجة النجاح",
    )
    max_marks = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=100,
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
        verbose_name="الدرجة النهائية",
    )

    class Meta:
        verbose_name = "مادة"
        verbose_name_plural = "المواد"
        ordering = ["level", "name"]

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name="الطالب",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name="المادة",
    )
    enrollment_date = models.DateField(auto_now_add=True, verbose_name="تاريخ التسجيل")
    grade = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="الدرجة النهائية",
    )
    attendance_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="نسبة الحضور",
    )

    class Meta:
        verbose_name = "تسجيل"
        verbose_name_plural = "التسجيلات"
        unique_together = ["student", "course"]
        ordering = ["-enrollment_date"]

    def __str__(self):
        return f"{self.student.name} - {self.course.name}"

    def get_grade_status(self):
        if self.grade is None:
            return "قيد الرصد"
        if self.grade >= self.course.pass_mark:
            return "ناجح"
        return "راسب"


class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ("present", "حاضر"),
        ("late", "متأخر"),
        ("excused", "بعذر"),
        ("absent", "غائب"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendance_records",
        verbose_name="الطالب",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="attendance_records",
        verbose_name="المادة",
    )
    date = models.DateField(default=timezone.localdate, verbose_name="التاريخ")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name="الحالة")
    notes = models.CharField(max_length=255, blank=True, verbose_name="ملاحظات")

    class Meta:
        verbose_name = "سجل حضور"
        verbose_name_plural = "سجلات الحضور"
        ordering = ["-date", "student__name"]
        unique_together = ["student", "course", "date"]

    def __str__(self):
        return f"{self.student.name} - {self.date}"


class Assessment(models.Model):
    TERM_CHOICES = [
        ("term1", "الفصل الأول"),
        ("term2", "الفصل الثاني"),
        ("final", "نهائي"),
    ]
    TYPE_CHOICES = [
        ("quiz", "اختبار قصير"),
        ("exam", "اختبار"),
        ("assignment", "واجب"),
        ("project", "مشروع"),
        ("participation", "مشاركة"),
    ]

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="assessments",
        verbose_name="المادة",
    )
    title = models.CharField(max_length=120, verbose_name="اسم التقييم")
    assessment_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name="نوع التقييم",
    )
    term = models.CharField(max_length=10, choices=TERM_CHOICES, verbose_name="الفصل")
    max_score = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=100,
        validators=[MinValueValidator(1)],
        verbose_name="الدرجة العظمى",
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="الوزن النسبي %",
    )
    due_date = models.DateField(verbose_name="تاريخ التقييم")
    instructions = models.TextField(blank=True, verbose_name="تعليمات")

    class Meta:
        verbose_name = "تقييم"
        verbose_name_plural = "التقييمات"
        ordering = ["-due_date", "course__name"]

    def __str__(self):
        return f"{self.course.name} - {self.title}"


class GradeRecord(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="grade_records",
        verbose_name="الطالب",
    )
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="grade_records",
        verbose_name="التقييم",
    )
    score = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="الدرجة المحققة",
    )
    feedback = models.TextField(blank=True, verbose_name="ملاحظات الأستاذ")
    graded_at = models.DateField(default=timezone.localdate, verbose_name="تاريخ الرصد")

    class Meta:
        verbose_name = "رصد درجة"
        verbose_name_plural = "رصد الدرجات"
        ordering = ["-graded_at"]
        unique_together = ["student", "assessment"]

    def __str__(self):
        return f"{self.student.name} - {self.assessment.title}"

    @property
    def percentage(self):
        if not self.assessment.max_score:
            return Decimal("0.00")
        return round((self.score / self.assessment.max_score) * 100, 2)

    @property
    def status(self):
        return "ممتاز" if self.percentage >= 90 else "جيد" if self.percentage >= 75 else "بحاجة دعم"


class FeeCategory(models.Model):
    name = models.CharField(max_length=80, unique=True, verbose_name="اسم البند المالي")
    description = models.TextField(blank=True, verbose_name="الوصف")
    default_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="المبلغ الافتراضي",
    )

    class Meta:
        verbose_name = "بند مالي"
        verbose_name_plural = "البنود المالية"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Invoice(models.Model):
    STATUS_CHOICES = [
        ("draft", "مسودة"),
        ("pending", "مستحقة"),
        ("partial", "مدفوعة جزئيًا"),
        ("paid", "مدفوعة"),
        ("overdue", "متأخرة"),
    ]

    invoice_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        editable=False,
        verbose_name="رقم الفاتورة",
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="invoices",
        verbose_name="الطالب",
    )
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="invoices",
        verbose_name="العام الدراسي",
    )
    category = models.ForeignKey(
        FeeCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="invoices",
        verbose_name="البند المالي",
    )
    title = models.CharField(max_length=120, verbose_name="عنوان الفاتورة")
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="المبلغ",
    )
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="الخصم",
    )
    due_date = models.DateField(verbose_name="تاريخ الاستحقاق")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="الحالة",
    )
    notes = models.TextField(blank=True, verbose_name="ملاحظات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        verbose_name = "فاتورة"
        verbose_name_plural = "الفواتير"
        ordering = ["due_date", "-created_at"]

    def __str__(self):
        return f"{self.title} - {self.student.name}"

    @property
    def total_after_discount(self):
        return max(self.amount - self.discount, Decimal("0.00"))

    @property
    def paid_amount(self):
        if not self.pk:
            return Decimal("0.00")
        return self.payments.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    @property
    def balance_due(self):
        return max(self.total_after_discount - self.paid_amount, Decimal("0.00"))

    def refresh_status(self):
        today = timezone.localdate()
        if self.balance_due <= 0:
            self.status = "paid"
        elif self.paid_amount > 0:
            self.status = "partial"
        elif self.due_date < today:
            self.status = "overdue"
        elif self.status == "draft":
            self.status = "draft"
        else:
            self.status = "pending"

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            year_seed = (
                self.academic_year.start_date.year
                if self.academic_year and self.academic_year.start_date
                else timezone.localdate().year
            )
            self.invoice_number = build_sequential_code(Invoice, "invoice_number", f"INV-{year_seed}-")
        self.refresh_status()
        super().save(*args, **kwargs)


class Payment(models.Model):
    METHOD_CHOICES = [
        ("cash", "نقدي"),
        ("transfer", "تحويل"),
        ("card", "بطاقة"),
    ]

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="الفاتورة",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="المبلغ المدفوع",
    )
    payment_date = models.DateField(default=timezone.localdate, verbose_name="تاريخ الدفع")
    method = models.CharField(max_length=10, choices=METHOD_CHOICES, verbose_name="طريقة الدفع")
    reference_number = models.CharField(max_length=50, blank=True, verbose_name="رقم المرجع")
    notes = models.TextField(blank=True, verbose_name="ملاحظات")

    class Meta:
        verbose_name = "دفعة"
        verbose_name_plural = "الدفعات"
        ordering = ["-payment_date", "-id"]

    def __str__(self):
        return f"{self.invoice.title} - {self.amount}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        invoice = self.invoice
        invoice.refresh_status()
        invoice.save(update_fields=["status"])


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("admin", "مدير"),
        ("accountant", "محاسب"),
        ("teacher", "معلم"),
        ("guardian", "ولي أمر"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name="المستخدم")
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, verbose_name="الدور")
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profiles",
        verbose_name="الأستاذ المرتبط",
    )
    guardian = models.ForeignKey(
        Guardian,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profiles",
        verbose_name="ولي الأمر المرتبط",
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profiles",
        verbose_name="الطالب المرتبط",
    )

    class Meta:
        verbose_name = "ملف مستخدم"
        verbose_name_plural = "ملفات المستخدمين"

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

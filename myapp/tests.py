from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import (
    AcademicYear,
    Course,
    FeeCategory,
    GradeRecord,
    Invoice,
    Payment,
    Student,
    Teacher,
)


class DashboardViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="secret123",
        )
        self.client.force_login(self.user)
        self.year = AcademicYear.objects.create(
            name="2025-2026",
            start_date=timezone.localdate(),
            end_date=timezone.localdate() + timedelta(days=250),
            is_current=True,
        )
        self.teacher = Teacher.objects.create(
            employee_id="T-01",
            name="سارة خالد",
            specialization="رياضيات",
        )
        self.student = Student.objects.create(
            name="أحمد سالم",
            gender="M",
            level="4",
            birth_date=timezone.localdate() - timedelta(days=3650),
            academic_year=self.year,
        )
        self.course = Course.objects.create(
            code="MATH4",
            name="الرياضيات",
            credit_hours=4,
            level="4",
            teacher=self.teacher,
            academic_year=self.year,
        )

    def test_dashboard_page_loads(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "لوحة القيادة المدرسية")

    def test_student_list_page_loads(self):
        response = self.client.get(reverse("student_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.student.name)

    def test_student_id_is_generated_automatically(self):
        self.assertRegex(self.student.student_id, r"^STU-\d{4}-\d{4}$")


class FinanceModelTests(TestCase):
    def test_invoice_status_updates_after_payment(self):
        year = AcademicYear.objects.create(
            name="2026-2027",
            start_date=timezone.localdate(),
            end_date=timezone.localdate() + timedelta(days=250),
        )
        category = FeeCategory.objects.create(name="رسوم دراسية", default_amount=Decimal("500"))
        student = Student.objects.create(
            name="ليان عمر",
            gender="F",
            level="6",
            birth_date=timezone.localdate() - timedelta(days=4000),
            academic_year=year,
        )
        invoice = Invoice.objects.create(
            student=student,
            academic_year=year,
            category=category,
            title="القسط الأول",
            amount=Decimal("500"),
            discount=Decimal("50"),
            due_date=timezone.localdate() + timedelta(days=5),
        )

        self.assertEqual(invoice.status, "pending")
        self.assertTrue(invoice.invoice_number.startswith("INV-2026-"))

        Payment.objects.create(
            invoice=invoice,
            amount=Decimal("450"),
            method="cash",
        )
        invoice.refresh_from_db()
        self.assertEqual(invoice.status, "paid")

    def test_gradebook_page_loads(self):
        user = User.objects.create_superuser(
            username="root",
            email="root@example.com",
            password="secret123",
        )
        self.client.force_login(user)
        year = AcademicYear.objects.create(
            name="2027-2028",
            start_date=timezone.localdate(),
            end_date=timezone.localdate() + timedelta(days=250),
        )
        teacher = Teacher.objects.create(employee_id="T-02", name="محمد نور", specialization="علوم")
        student = Student.objects.create(
            name="أروى عبدالله",
            gender="F",
            level="5",
            birth_date=timezone.localdate() - timedelta(days=3900),
            academic_year=year,
        )
        course = Course.objects.create(
            code="SCI5",
            name="العلوم",
            credit_hours=3,
            level="5",
            teacher=teacher,
            academic_year=year,
        )
        assessment = course.assessments.create(
            title="اختبار الوحدة",
            assessment_type="exam",
            term="term1",
            max_score=100,
            weight=25,
            due_date=timezone.localdate(),
        )
        GradeRecord.objects.create(student=student, assessment=assessment, score=88)

        response = self.client.get(reverse("gradebook_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "دفتر الدرجات")

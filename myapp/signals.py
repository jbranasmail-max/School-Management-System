from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver


ROLE_PERMISSIONS = {
    "مدير": None,
    "محاسب": {
        "view_student",
        "view_guardian",
        "view_invoice",
        "add_invoice",
        "change_invoice",
        "view_payment",
        "add_payment",
        "change_payment",
        "view_feecategory",
        "add_feecategory",
        "change_feecategory",
        "view_academicyear",
    },
    "معلم": {
        "view_student",
        "view_teacher",
        "view_course",
        "view_enrollment",
        "view_assessment",
        "add_assessment",
        "change_assessment",
        "view_graderecord",
        "add_graderecord",
        "change_graderecord",
        "view_attendancerecord",
        "add_attendancerecord",
        "change_attendancerecord",
    },
    "ولي أمر": {
        "view_student",
        "view_invoice",
        "view_payment",
        "view_graderecord",
        "view_attendancerecord",
        "view_enrollment",
    },
}


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    if sender.name != "myapp":
        return

    all_permissions = Permission.objects.all()
    for group_name, permission_codes in ROLE_PERMISSIONS.items():
        group, _ = Group.objects.get_or_create(name=group_name)
        if permission_codes is None:
            group.permissions.set(all_permissions)
        else:
            group.permissions.set(Permission.objects.filter(codename__in=permission_codes))

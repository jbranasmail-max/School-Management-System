from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "myapp"

    def ready(self):
        from django.db.utils import OperationalError
        from django.db import ProgrammingError
        from datetime import date

        try:
            from .models import AcademicYear

            for year in range(2020, 2051):

                hijri_year = 1435 + (year - 2020)

                AcademicYear.objects.get_or_create(
                    name=f"{year}-{year + 1}",
                    defaults={
                        "start_date": date(year, 9, 1),
                        "end_date": date(year + 1, 6, 30),
                        "hijri_year": hijri_year,
                        "is_current": False,
                    }
                )

        except (OperationalError, ProgrammingError):
            pass
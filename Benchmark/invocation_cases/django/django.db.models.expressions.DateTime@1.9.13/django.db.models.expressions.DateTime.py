import django
from django.conf import settings
from django.db import models
from django.db.models.expressions import DateTime
from django.utils import timezone
import inspect

settings.configure(
    DEBUG=True,
    USE_TZ=True,
    INSTALLED_APPS=[],
)
django.setup()

def main():
    dt_expr = DateTime(
        lookup="created_at",
        lookup_type="year",
        tzinfo=timezone.get_current_timezone(),
    )
    print("DateTime expression:", dt_expr)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(DateTime))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
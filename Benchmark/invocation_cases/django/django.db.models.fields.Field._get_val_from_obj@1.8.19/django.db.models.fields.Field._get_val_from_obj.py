import django
from django.conf import settings
from django.db import models
from django.db.models import Field
import inspect

settings.configure(
    INSTALLED_APPS=[
        '__main__'
    ]
)
django.setup()

class MyModel(models.Model):
    my_field = models.CharField(max_length=100)

    class Meta:
        app_label = '__main__'

def main():
    instance = MyModel(my_field="test value")
    field = instance._meta.get_field('my_field')
    result = Field._get_val_from_obj(field,instance)
    print("_get_val_from_obj result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Field._get_val_from_obj))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
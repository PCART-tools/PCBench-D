import inspect
import django
from django.conf import settings

settings.configure()
django.setup()

def main():
    from django.db.backends.oracle.base import DatabaseWrapper
    from django.db.backends.oracle.operations import DatabaseOperations

    fake_settings_dict = {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {},
    }

    wrapper = DatabaseWrapper(fake_settings_dict)
    db_operations = wrapper.ops

    result = DatabaseOperations.return_insert_id(db_operations)
    
    print("return_insert_id result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(DatabaseOperations.return_insert_id))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()

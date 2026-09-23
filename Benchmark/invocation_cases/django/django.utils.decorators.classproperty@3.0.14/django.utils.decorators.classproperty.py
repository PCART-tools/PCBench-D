import inspect
from django.utils.decorators import classproperty

class MyClass:
    _value = "Hello, classproperty!"

    @classproperty
    def value(cls):
        return cls._value

def main():
    # Call the target API
    result = MyClass.value
    print("classproperty result:", result)

    # Get the source code of the target API
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(classproperty))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
import inspect
from django.utils.functional import allow_lazy

def example_function():
    return "Hello, World!"

def main():
    lazy_function = allow_lazy(example_function, str)
    result = lazy_function()
    print("allow_lazy result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(allow_lazy))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
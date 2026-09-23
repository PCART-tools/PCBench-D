import matplotlib.rcsetup as rcsetup
import inspect

def main():
    backend = 'TkAgg'
    result = rcsetup.validate_backend(backend)
    print("validate_backend result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(rcsetup.validate_backend))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
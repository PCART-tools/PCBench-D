import matplotlib.cbook as cbook
import inspect

def main():
    # Create an instance of the MatplotlibDeprecationWarning
    warning_instance = cbook.deprecation.MatplotlibDeprecationWarning("This is a test warning.")
    print("MatplotlibDeprecationWarning instance:", warning_instance)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(cbook.deprecation.MatplotlibDeprecationWarning))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
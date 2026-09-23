import matplotlib.cbook as cbook
import inspect

def main():
    # Simulate a deprecated warning
    cbook.warn_deprecated("3.3", message="This is a test deprecation warning.")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(cbook.warn_deprecated))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
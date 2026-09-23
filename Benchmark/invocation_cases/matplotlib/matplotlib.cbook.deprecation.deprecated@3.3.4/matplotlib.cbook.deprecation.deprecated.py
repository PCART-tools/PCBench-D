import matplotlib.cbook.deprecation as mcd
import inspect

def main():
    @mcd.deprecated("3.3.4", alternative="new_function")
    def old_function():
        return "This is a deprecated function."

    result = old_function()
    print("Deprecated function result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mcd.deprecated))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
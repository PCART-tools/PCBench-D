import numpy as np
import inspect

def main():
    def custom_string_function(x):
        return f"Custom representation: {x}"

    np.set_string_function(custom_string_function, repr=True)
    arr = np.array([1, 2, 3])
    print("Custom string representation:", repr(arr))

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(np.set_string_function))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
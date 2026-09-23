import numpy as np
import inspect

def main():
    array_types = [np.int32, np.float64]
    scalar_types = [np.int64]
    result = np.find_common_type(array_types, scalar_types)
    print("find_common_type result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(np.find_common_type))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
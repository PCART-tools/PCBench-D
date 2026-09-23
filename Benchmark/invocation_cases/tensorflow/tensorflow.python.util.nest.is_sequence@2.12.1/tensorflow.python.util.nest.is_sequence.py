import tensorflow as tf
from tensorflow.python.util import nest
import inspect

def main():
    # Test data
    test_data = [1, 2, [3, 4], (5, 6)]
    result = nest.is_sequence(test_data)
    print("is_sequence result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(nest.is_sequence))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
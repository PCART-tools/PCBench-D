import numpy as np
import inspect

def main():
    complex_number = 3 + 4j
    data = np.array([complex_number])
    formatter = np.core.arrayprint.ComplexFormat(data, precision=2, suppress_small=False)
    result = formatter(complex_number)
    print("Formatted complex number:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(np.core.arrayprint.ComplexFormat))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()

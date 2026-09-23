import numpy as np
import inspect

def main():
    complex_number = np.array(
        [complex(np.longdouble(1), np.longdouble(2)),
         complex(np.longdouble(3), np.longdouble(4))],
        dtype=np.clongdouble
    )

    formatter = np.core.arrayprint.LongComplexFormat(precision=8)
    formatted = [formatter(x) for x in complex_number]

    print("Formatted complex numbers:", formatted)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(np.core.arrayprint.LongComplexFormat))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()

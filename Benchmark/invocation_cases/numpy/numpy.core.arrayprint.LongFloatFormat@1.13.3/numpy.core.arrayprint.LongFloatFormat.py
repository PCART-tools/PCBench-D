import numpy as np
import inspect

def main():
    class DummyFloat:
        def __float__(self):
            return 123.4567890123456789

    value = np.longdouble(float(DummyFloat()))
    formatter = np.core.arrayprint.LongFloatFormat(
        precision=10,
        sign=False
    )

    result = formatter(value)
    print("LongFloatFormat result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(np.core.arrayprint.LongFloatFormat))
    except Exception as e:
        print(type(e).__name__,e)

if __name__ == "__main__":
    main()

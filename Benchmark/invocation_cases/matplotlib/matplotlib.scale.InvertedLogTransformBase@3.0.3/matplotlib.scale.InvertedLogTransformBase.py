import numpy as np
import inspect
from matplotlib.scale import InvertedLogTransformBase

class DummyInvertedLogTransform(InvertedLogTransformBase):
    base = 10.0

    def inverted(self):
        return Log10Transform()


def main():
    transform = DummyInvertedLogTransform()

    data = np.array([1.0, 10.0, 100.0])
    result = transform.transform(data)

    print("InvertedLogTransformBase result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(InvertedLogTransformBase))
    except Exception as e:
        print(type(e).__name__)


if __name__ == "__main__":
    main()
import matplotlib.scale as mscale
import inspect
from matplotlib.scale import LogTransformBase

class DummyTransform(LogTransformBase):
    base = 10.0

    def inverted(self):
        return InvertedLog10Transform()

def main():
    transform = DummyTransform()
    result = transform.transform([1, 10, 100])
    print("LogTransform result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(LogTransformBase))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
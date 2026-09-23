import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axis_artist import BezierPath
import inspect

def main():
    path = BezierPath([(0, 0), (1, 2), (2, 3)])
    print("BezierPath:", path)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(BezierPath))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axislines import Axes
import inspect

def main():
    fig = plt.figure()
    ax = Axes(fig, [0.1, 0.1, 0.8, 0.8])
    fig.add_axes(ax)

    AxisDict = Axes.AxisDict  # 正确访问内部类
    axis_dict = AxisDict(ax)
    print("AxisDict keys:", list(axis_dict.keys()))

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(AxisDict))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()

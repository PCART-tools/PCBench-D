import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.axes_rgb import RGBAxesBase
import inspect

def main():
    fig = plt.figure()
    ax = RGBAxesBase(fig, [0.1, 0.1, 0.8, 0.8])
    print("RGBAxesBase instance created:", ax)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(RGBAxesBase))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
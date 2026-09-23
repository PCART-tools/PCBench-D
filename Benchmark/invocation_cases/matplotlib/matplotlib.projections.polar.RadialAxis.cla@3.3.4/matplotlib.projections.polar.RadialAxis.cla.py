import matplotlib.pyplot as plt
from matplotlib.projections.polar import RadialAxis
import inspect

class MyRadialAxis(RadialAxis):
    pass

def main():
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    RadialAxis.cla(ax.yaxis)
    print("cla called successfully.")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(RadialAxis.cla))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
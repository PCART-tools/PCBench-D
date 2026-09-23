import matplotlib.pyplot as plt
from matplotlib.projections.polar import ThetaAxis
import inspect

class MyRadialAxis(ThetaAxis):
    pass

def main():
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.yaxis.__class__ = MyRadialAxis

    ThetaAxis.cla(ax.yaxis)
    print("cla called successfully.")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ThetaAxis.cla))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
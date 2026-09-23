import matplotlib.pyplot as plt
import numpy as np
import matplotlib.contour as contour
from matplotlib.contour import ContourSet
import inspect

def main():
    x = y = np.linspace(-3, 3, 20)
    X, Y = np.meshgrid(x, y)
    Z = X**2 + Y**2

    fig, ax = plt.subplots()
    cs = ax.contour(X, Y, Z, levels=[1, 2, 3])
    cs.clabel(levels=[1, 2, 3])
    contour.ContourLabeler.add_label_clabeltext(
        cs,
        x=0.5,
        y=0.5,
        rotation=0,
        lev=2,
        cvalue=2,
    )
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(contour.ContourLabeler.add_label_clabeltext))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
import matplotlib.pyplot as plt
import numpy as np
import inspect
from matplotlib.contour import ClabelText

def main():
    # Create a simple contour plot
    x = np.linspace(-3.0, 3.0, 100)
    y = np.linspace(-3.0, 3.0, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))

    fig, ax = plt.subplots()
    CS = ax.contour(X, Y, Z)
    level = CS.levels[0]
    label = ClabelText(
        x=0.0,
        y=0.0,
        text=str(level),
        color='black',
        rotation=0,
        ha='center',
        va='center'
    )

    print("ClabelText used in clabels:", label)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ClabelText))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
import inspect
import matplotlib.pyplot as plt
from matplotlib.colorbar import ColorbarPatch
from matplotlib.cm import ScalarMappable


def main():
    fig, ax = plt.subplots()

    mappable = ScalarMappable()
    mappable.set_array([])
    mappable.hatches = ['']

    colorbar = ColorbarPatch(ax, mappable)
    print("ColorbarPatch created:", colorbar)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ColorbarPatch))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
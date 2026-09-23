import matplotlib.colors as mcolors
import matplotlib.colorbar as mcolorbar
import inspect

def main():
    dummy = mcolorbar._ColorbarMappableDummy()
    new_norm = mcolors.Normalize(vmin=10, vmax=20)
    dummy.set_norm(new_norm)

    print("set_norm applied with new normalization:", new_norm)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(dummy.set_norm))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import SubplotDivider
import inspect

def main():
    fig = plt.figure()
    divider = SubplotDivider(fig, 1, 1, 1)
    divider.change_geometry(2, 2, 1)
    print("change_geometry called successfully.")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(SubplotDivider.change_geometry))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import SubplotDivider
import inspect

def main():
    fig = plt.figure()
    divider = SubplotDivider(fig, 1, 1, 1)
    geometry = divider.get_geometry()
    print("get_geometry result:", geometry)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(SubplotDivider.get_geometry))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
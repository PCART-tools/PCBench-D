import matplotlib.pyplot as plt
import matplotlib.colorbar as cbar
import numpy as np
import inspect

def main():
    fig, ax = plt.subplots()
    norm = plt.Normalize(vmin=0, vmax=1)
    cb = cbar.ColorbarBase(ax, norm=norm, orientation='horizontal')
    cmap = cb.get_cmap()
    print("get_cmap result:", cmap)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(cbar.ColorbarBase.get_cmap))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
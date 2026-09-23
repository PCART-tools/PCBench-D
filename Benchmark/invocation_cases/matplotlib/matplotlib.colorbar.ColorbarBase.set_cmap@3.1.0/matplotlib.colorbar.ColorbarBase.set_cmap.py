import matplotlib.pyplot as plt
import matplotlib.colorbar as cbar
import matplotlib.colors as mcolors
import inspect

def main():
    fig, ax = plt.subplots()
    norm = mcolors.Normalize(vmin=0, vmax=100)
    colorbar = cbar.ColorbarBase(ax, norm=norm, orientation='horizontal')
    
    cmap = plt.cm.viridis
    colorbar.set_cmap(cmap)
    print("set_cmap called successfully with cmap:", cmap.name)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(cbar.ColorbarBase.set_cmap))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
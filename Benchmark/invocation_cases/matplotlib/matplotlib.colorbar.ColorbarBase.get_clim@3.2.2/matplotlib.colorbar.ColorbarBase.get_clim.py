import matplotlib.pyplot as plt
import numpy as np
import inspect
from matplotlib.colors import Normalize
from matplotlib.colorbar import ColorbarBase

def main():
    fig, ax = plt.subplots()
    data = np.random.rand(10, 10)
    cax = ax.imshow(data, cmap='viridis')
    colorbar = ColorbarBase(ax=ax, cmap=plt.get_cmap('viridis'), norm=Normalize(vmin=data.min(), vmax=data.max()))
    clim = colorbar.get_clim()
    print("get_clim result:", clim)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ColorbarBase.get_clim))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
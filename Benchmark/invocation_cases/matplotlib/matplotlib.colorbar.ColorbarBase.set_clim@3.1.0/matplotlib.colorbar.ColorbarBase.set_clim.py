import matplotlib.pyplot as plt
import numpy as np
import inspect
from matplotlib.colorbar import ColorbarBase

class TestColorbar(ColorbarBase):
    pass

def main():
    fig, ax = plt.subplots()

    data = np.random.rand(10, 10)
    im = ax.imshow(data, cmap="viridis")

    cbar = TestColorbar(
        ax=ax,
        cmap=im.get_cmap(),
        norm=im.norm,
        orientation="vertical"
    )

    cbar.set_clim(0, 1)
    print("set_clim result: Color limits set to (0, 1)")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(cbar.set_clim))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
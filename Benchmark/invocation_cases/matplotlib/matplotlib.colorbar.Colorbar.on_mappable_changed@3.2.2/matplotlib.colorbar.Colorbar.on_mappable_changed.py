import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import inspect

def main():
    fig, ax = plt.subplots()
    data = np.random.rand(10, 10)
    cax = ax.imshow(data, cmap='viridis')
    colorbar = plt.colorbar(cax)
    colorbar.on_mappable_changed(cax)
    print("on_mappable_changed called successfully.")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(colorbar.on_mappable_changed))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
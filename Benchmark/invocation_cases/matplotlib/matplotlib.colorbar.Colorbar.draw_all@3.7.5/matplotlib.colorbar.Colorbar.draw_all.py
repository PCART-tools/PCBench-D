import matplotlib.pyplot as plt
import numpy as np
import inspect

def main():
    # Create a simple plot with a colorbar
    data = np.random.rand(10, 10)
    fig, ax = plt.subplots()
    cax = ax.imshow(data, cmap='viridis')
    colorbar = fig.colorbar(cax)

    # Call the draw_all method
    colorbar.draw_all()
    print("draw_all called successfully.")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(colorbar.draw_all))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import inspect

def main():
    # Create a figure and axis
    fig, ax = plt.subplots()
    
    # Create a simple plot with a colorbar
    data = np.random.rand(10, 10)
    cax = ax.imshow(data, cmap='viridis')
    colorbar = fig.colorbar(cax, ax=ax)
    
    # Call the target API
    colorbar.update_bruteforce(colorbar.mappable)
    print("update_bruteforce called successfully")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(colorbar.update_bruteforce))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
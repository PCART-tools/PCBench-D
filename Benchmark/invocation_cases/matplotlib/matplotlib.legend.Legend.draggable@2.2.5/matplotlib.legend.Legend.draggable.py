import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import inspect
from matplotlib.legend import Legend

def main():
    # Create a simple plot with a legend
    fig, ax = plt.subplots()
    line, = ax.plot([1, 2, 3], label='Line')
    legend = ax.legend()

    # Call the draggable method
    result = Legend.draggable(legend,True)
    print("draggable result:", result)


    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Legend.draggable))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
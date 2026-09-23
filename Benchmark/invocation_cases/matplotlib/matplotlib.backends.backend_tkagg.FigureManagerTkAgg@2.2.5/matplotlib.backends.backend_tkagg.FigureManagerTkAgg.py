import matplotlib
import tkinter as tk
import inspect
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg

def main():
    root = tk.Tk()
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])

    canvas = tkagg.FigureCanvasTkAgg(fig, master=root)
    manager = tkagg.FigureManagerTkAgg(canvas,1, root)
    print("FigureManagerTkAgg created:", manager)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tkagg.FigureManagerTkAgg))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
import matplotlib
import matplotlib.backends.backend_tkagg as tkagg
import inspect
import tkinter as tk

def main():
    root = tk.Tk()
    root.withdraw()  # Prevent Tkinter window from appearing

    canvas = tkagg.FigureCanvasTkAgg(matplotlib.figure.Figure(), master=root)

    toolbar = tkagg.NavigationToolbar2TkAgg(canvas, root)
    toolbar.update()
    print("NavigationToolbar2Tk created:", toolbar)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tkagg.NavigationToolbar2TkAgg))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
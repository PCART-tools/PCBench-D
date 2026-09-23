import inspect
from matplotlib.figure import Figure
from matplotlib.backend_bases import FigureCanvasBase, MouseEvent

class MyCanvas(FigureCanvasBase):
    def __init__(self, figure):
        super().__init__(figure)

def main():
    fig = Figure()
    canvas = MyCanvas(fig)
    mouse_event = MouseEvent(
        name='button_press_event',
        canvas=canvas,
        x=0,
        y=0,
        button=1
    )

    result = canvas.pick(mouse_event)
    print("pick result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(canvas.pick))
    except Exception as e:
        print(type(e).__name__, e)

if __name__ == "__main__":
    main()
import matplotlib
matplotlib.use("Agg")

import inspect
from matplotlib.backends.backend_agg import FigureCanvasAgg, RendererAgg

def main():
    canvas = FigureCanvasAgg(None)
    renderer = RendererAgg(100, 100, 100)
    canvas.renderer = renderer     
    canvas._renderer = renderer   
    rgb = canvas.tostring_rgb()
    print("tostring_rgb result length:", len(rgb))

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(canvas.tostring_rgb))
    except Exception as e:
        print(type(e).__name__)    


if __name__ == "__main__":
    main()

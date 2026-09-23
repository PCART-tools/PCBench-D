import matplotlib
matplotlib.use("svg")  # headless-safe

import matplotlib.backends.backend_svg as svg
import numpy as np
import inspect
from matplotlib.transforms import IdentityTransform
from io import StringIO

def main():
    buffer = StringIO()
    renderer = svg.RendererSVG(200, 200, buffer)

    points = np.array([[0.0, 0.0],
                       [1.0, 0.0],
                       [0.5, 1.0]])
    colors = np.array([[1, 0, 0, 1],
                       [0, 1, 0, 1],
                       [0, 0, 1, 1]])
    transform = IdentityTransform()

    
    renderer.draw_gouraud_triangle(None, points, colors, transform)
    print("draw_gouraud_triangle call succeeded")


    print("-----getsource_output-----")
    try:
        print(inspect.getsource(renderer.draw_gouraud_triangle))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()

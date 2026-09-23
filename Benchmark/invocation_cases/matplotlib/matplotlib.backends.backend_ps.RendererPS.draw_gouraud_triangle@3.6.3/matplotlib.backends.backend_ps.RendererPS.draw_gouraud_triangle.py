import numpy as np
from matplotlib.backends.backend_ps import RendererPS
from matplotlib.transforms import Affine2D
import io
import inspect



def main():
    ps_buffer = io.StringIO()
    renderer = RendererPS(
        width=400,
        height=400,
        pswriter=ps_buffer,
    )
    gc = renderer.new_gc()
    points = np.array([
        [100.0, 100.0],
        [300.0, 100.0],
        [200.0, 300.0],
    ], dtype=float)

    colors = np.array([
        [1.0, 0.0, 0.0, 1.0],  # red
        [0.0, 1.0, 0.0, 1.0],  # green
        [0.0, 0.0, 1.0, 1.0],  # blue
    ], dtype=float)
    transform = Affine2D()
    RendererPS.draw_gouraud_triangle(
        renderer,
        gc,
        points,
        colors,
        transform
    )
    print("draw_gouraud_triangle called successfully")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(RendererPS.draw_gouraud_triangle))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
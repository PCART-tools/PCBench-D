import matplotlib
matplotlib.use("Agg")

import inspect
from matplotlib.backends.backend_agg import RendererAgg

def main():
    renderer = RendererAgg(100, 100, 100)

    rgb = renderer.tostring_rgb()
    print("tostring_rgb result length:", len(rgb))

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(renderer.tostring_rgb))
    except Exception as e:
        print(type(e).__name__)    

if __name__ == "__main__":
    main()

import matplotlib
from matplotlib.backends.backend_gtk3cairo import RendererGTK3Cairo
import inspect

def main():
    renderer = RendererGTK3Cairo(dpi=100)
    print("RendererGTK3Cairo instance:", renderer)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(RendererGTK3Cairo))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
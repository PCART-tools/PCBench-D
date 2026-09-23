import matplotlib.backends.backend_cairo as backend_cairo
import cairo
import inspect

def main():
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 100, 100)
    renderer = backend_cairo.RendererCairo(surface)  # Assuming initialized without dpi
    result = renderer.set_ctx_from_surface(surface)
    print("set_ctx_from_surface result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(backend_cairo.RendererCairo.set_ctx_from_surface))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
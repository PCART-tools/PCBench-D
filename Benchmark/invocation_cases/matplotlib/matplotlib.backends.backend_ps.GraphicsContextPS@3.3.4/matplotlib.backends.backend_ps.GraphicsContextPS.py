import matplotlib.backends.backend_ps as backend_ps
import inspect

def main():
    gc_ps = backend_ps.GraphicsContextPS()
    print("GraphicsContextPS instance:", gc_ps)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(backend_ps.GraphicsContextPS))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
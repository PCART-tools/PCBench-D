import matplotlib.backends.backend_pgf as backend_pgf
import inspect

def main():
    gc_pgf = backend_pgf.GraphicsContextPgf()
    print("GraphicsContextPgf instance:", gc_pgf)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(backend_pgf.GraphicsContextPgf))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
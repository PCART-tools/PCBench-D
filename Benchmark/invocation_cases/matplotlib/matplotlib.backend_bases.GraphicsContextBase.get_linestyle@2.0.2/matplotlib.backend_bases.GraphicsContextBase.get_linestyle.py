import matplotlib.backend_bases as mbb
import inspect

def main():
    gc = mbb.GraphicsContextBase()
    gc._linestyle = None  # Set a default linestyle
    linestyle = gc.get_linestyle(gc._linestyle)
    print("get_linestyle result:", linestyle)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mbb.GraphicsContextBase.get_linestyle))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
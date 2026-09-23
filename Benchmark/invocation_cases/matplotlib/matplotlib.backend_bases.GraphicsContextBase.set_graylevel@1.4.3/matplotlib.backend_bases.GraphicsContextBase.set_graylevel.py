import matplotlib.backend_bases as mbb
import inspect

def main():
    gc = mbb.GraphicsContextBase()

    gc.set_graylevel(0.5)
    print("set_graylevel called successfully.")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mbb.GraphicsContextBase.set_graylevel))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
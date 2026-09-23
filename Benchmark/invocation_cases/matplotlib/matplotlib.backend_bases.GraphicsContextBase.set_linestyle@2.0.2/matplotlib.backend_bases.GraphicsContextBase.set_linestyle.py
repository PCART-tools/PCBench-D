import matplotlib.backend_bases as mbb
import inspect

def main():
    gc = mbb.GraphicsContextBase()
    gc.set_linestyle('dashed')
    print("set_linestyle invoked successfully")


    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mbb.GraphicsContextBase.set_linestyle))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
import inspect
from matplotlib.mathtext import SsGlue

def main():
    ss_glue = SsGlue()
    print("Glue instance:", ss_glue)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(SsGlue))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
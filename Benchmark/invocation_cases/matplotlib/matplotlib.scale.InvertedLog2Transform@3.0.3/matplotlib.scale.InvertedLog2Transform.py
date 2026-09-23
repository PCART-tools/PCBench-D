import matplotlib.scale as mscale
import inspect

def main():
    transform = mscale.InvertedLog2Transform()
    print("InvertedLog2Transform instance:", transform)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mscale.InvertedLog2Transform))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
import matplotlib.scale as mscale
import inspect

def main():
    transform = mscale.InvertedNaturalLogTransform()
    print("InvertedNaturalLogTransform instance:", transform)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mscale.InvertedNaturalLogTransform))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()